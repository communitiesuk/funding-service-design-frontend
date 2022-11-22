from functools import wraps
from http.client import METHOD_NOT_ALLOWED
import requests
from app.constants import ApplicationStatus
from app.default.data import get_account
from app.default.data import get_application_data
from app.default.data import get_applications_for_account
from app.default.data import get_fund_data
from app.default.data import get_round_data
from app.default.data import get_round_data_fail_gracefully
from app.helpers import format_rehydrate_payload
from app.helpers import get_token_to_return_to_application
from app.models.application_summary import ApplicationSummary
from config import Config
from flask import abort
from flask import Blueprint
from flask import current_app
from flask import g
from flask import redirect
from flask import render_template
from flask import request
from flask import url_for
from flask_wtf import FlaskForm
from flask_wtf.csrf import CSRFError
from fsd_utils.authentication.decorators import login_requested
from fsd_utils.authentication.decorators import login_required
from fsd_utils.locale_selector.get_lang import get_lang
from flask_babel import force_locale


default_bp = Blueprint("routes", __name__, template_folder="templates")


# TODO Move the following method into utils.
# Utils will need a way of accessing application data.


def verify_application_owner_local(f):
    """
    This decorator determines whether the user trying to access an application
    is the owner of that application. If they are, passes through to the
    decorated method. If not, it returns a 401 response.

    It detects whether the call was a GET or a POST and reads the parameters
    accordingly.
    """

    @wraps(f)
    def decorator(*args, **kwargs):
        if request.method == "POST":
            application_id = request.form["application_id"]
        elif request.method == "GET":
            application_id = kwargs["application_id"]
        else:
            abort(
                METHOD_NOT_ALLOWED,
                f"Http method {request.method} is not supported",
            )

        application = get_application_data(application_id, as_dict=True)
        application_owner = application.account_id
        current_user = g.account_id
        if current_user == application_owner:
            return f(*args, **kwargs)
        else:
            abort(
                401,
                f"User {current_user} attempted to access application"
                f" {application_id}, owned by {application_owner}",
            )

    return decorator


# End TODO


@default_bp.route("/")
def index():
    current_app.logger.info("Service landing page loaded.")
    try:
        round_data = get_round_data(
            Config.DEFAULT_FUND_ID, Config.DEFAULT_ROUND_ID, as_dict=True
        )
        submission_deadline = round_data.deadline
        contact_us_email_address = round_data.contact_details["email_address"]
        round_title = round_data.title
    except:  # noqa
        round_title = ""
        submission_deadline = ""
        contact_us_email_address = ""

    return render_template(
        "index.html",
        service_url=Config.ENTER_APPLICATION_URL,
        round_title=round_title,
        submission_deadline=submission_deadline,
        contact_us_email_address=contact_us_email_address,
    )


@default_bp.route("/accessibility_statement", methods=["GET"])
def accessibility_statement():
    current_app.logger.info("Accessibility statement page loaded.")
    return render_template("accessibility_statement.html")


@default_bp.route("/cof_r2w2_all_questions", methods=["GET"])
def all_questions():
    current_app.logger.info("All questions page loaded.")
    return render_template("cof_r2w2_all_questions.html")


@default_bp.route("/contact_us", methods=["GET"])
def contact_us():
    current_app.logger.info("Contact us page loaded.")
    round_data = get_round_data_fail_gracefully(
        Config.DEFAULT_FUND_ID, Config.DEFAULT_ROUND_ID
    )
    return render_template("contact_us.html", round_data=round_data)


@default_bp.route("/cookie_policy", methods=["GET"])
def cookie_policy():
    current_app.logger.info("Cookie policy page loaded.")
    return render_template("cookie_policy.html")


@default_bp.route("/account")
@login_required
def dashboard():
    account_id = g.account_id
    application_store_response = get_applications_for_account(
        account_id=account_id, as_dict=False
    )
    applications: list[ApplicationSummary] = [
        ApplicationSummary.from_dict(application)
        for application in application_store_response
    ]
    if len(applications) > 0:
        round_id = applications[0].round_id
        fund_id = applications[0].fund_id
    else:
        round_id = Config.DEFAULT_ROUND_ID
        fund_id = Config.DEFAULT_FUND_ID

    current_app.logger.info(
        f"Setting up applicant dashboard for :'{account_id}' to apply for fund"
        f" {fund_id} on round {round_id}"
    )

    for application in applications:
        if application.status == "COMPLETED":
            application.status = "READY_TO_SUBMIT"

    return render_template(
        "dashboard.html",
        account_id=account_id,
        applications=applications,
        round_id=round_id,
        fund_id=fund_id,
    )


@default_bp.route("/account/new", methods=["POST"])
@login_required
def new():
    account_id = g.account_id
    new_application = requests.post(
        url=f"{Config.APPLICATION_STORE_API_HOST}/applications",
        json={
            "account_id": account_id,
            "round_id": request.form["round_id"] or Config.DEFAULT_ROUND_ID,
            "fund_id": request.form["fund_id"] or Config.DEFAULT_FUND_ID,
            "language": get_lang(),
        },
    )
    new_application_json = new_application.json()
    current_app.logger.info(f"Creating new application:{new_application_json}")
    if new_application.status_code != 201 or not new_application_json.get(
        "id"
    ):
        raise Exception(
            "Unexpected response from application store when creating new"
            " application: "
            + str(new_application.status_code)
        )
    return redirect(
        url_for(
            "routes.tasklist", application_id=new_application.json().get("id")
        )
    )


@default_bp.route("/tasklist/<application_id>", methods=["GET"])
@login_required
@verify_application_owner_local
def tasklist(application_id):
    """
    Returns a Flask function which constructs a tasklist for an application id.

    Args:
        application_id (str): the id of an application in the application store

    Returns:
        function: a function which renders the tasklist template.
    """
    application = get_application_data(application_id, as_dict=True)

    account = get_account(account_id=application.account_id)
    if application.status == ApplicationStatus.SUBMITTED.name:
        with force_locale(application.language):
            return render_template(
                "application_submitted.html",
                application_id=application.id,
                application_reference=application.reference,
                application_email=account.email,
            )
    fund = get_fund_data(application.fund_id, as_dict=True)
    round_data = get_round_data(
        Config.DEFAULT_FUND_ID, Config.DEFAULT_ROUND_ID, True
    )
    sections = application.get_sections()
    form = FlaskForm()
    application_meta_data = {
        "application_id": application_id,
        "fund_name": fund.name,
        "round_name": round_data.title,
        "not_started_status": ApplicationStatus.NOT_STARTED.name,
        "in_progress_status": ApplicationStatus.IN_PROGRESS.name,
        "completed_status": ApplicationStatus.COMPLETED.name,
        "submitted_status": ApplicationStatus.SUBMITTED.name,
        "number_of_forms": len(application.forms),
        "number_of_completed_forms": len(
            list(
                filter(
                    lambda form: form["status"]
                    == ApplicationStatus.COMPLETED.name,
                    application.forms,
                )
            )
        ),
    }
    
    with force_locale(application.language):
        return render_template(
            "tasklist.html",
            application=application,
            sections=sections,
            application_meta_data=application_meta_data,
            form=form,
            contact_us_email_address=round_data.contact_details["email_address"],
            submission_deadline=round_data.deadline,
        )


@default_bp.route("/continue_application/<application_id>", methods=["GET"])
@login_required
@verify_application_owner_local
def continue_application(application_id):
    """
    Returns a Flask function to return to an active application form.
    This provides a way of returning to an applicants partially completed
        application.

    Args:
        application_id (str): The id of an application in the application store
        form_name (str): The name of the application sub form
        page_name (str): The form page to redirect the user to.

    Returns:
        A function: given a users application id they are redirected to
        the specified application form page within the form runner service
    """
    args = request.args
    form_name = args.get("form_name")
    return_url = (
        request.host_url
        + url_for("routes.tasklist", application_id=application_id)[1:]
    )
    current_app.logger.info(
        f"Url the form runner should return to '{return_url}'."
    )

    application = get_application_data(application_id, as_dict=True)

    form_data = application.get_form_data(application, form_name)

    rehydrate_payload = format_rehydrate_payload(
        form_data, application_id, return_url, form_name
    )

    rehydration_token = get_token_to_return_to_application(
        form_name, rehydrate_payload
    )

    redirect_url = Config.FORM_REHYDRATION_URL.format(
        rehydration_token=rehydration_token
    )
    if Config.FORMS_SERVICE_PRIVATE_HOST:
        redirect_url = redirect_url.replace(
            Config.FORMS_SERVICE_PRIVATE_HOST, Config.FORMS_SERVICE_PUBLIC_HOST
        )
    current_app.logger.info("redirecting to form runner")
    return redirect(redirect_url)


@default_bp.route("/submit_application", methods=["POST"])
@login_required
@verify_application_owner_local
def submit_application():
    
    application_id = request.form.get("application_id")
    submitted = format_payload_and_submit_application(application_id)

    application_id = submitted.get("id")
    application_reference = submitted.get("reference")
    application_email = submitted.get("email")
    application = get_application_data(application_id, as_dict=True)
    with force_locale(application.language):
        return render_template(
            "application_submitted.html",
            application_id=application_id,
            application_reference=application_reference,
            application_email=application_email,
        )


def format_payload_and_submit_application(application_id):
    payload = {"application_id": application_id}
    submission_response = requests.post(
        Config.SUBMIT_APPLICATION_ENDPOINT.format(
            application_id=application_id
        ),
        json=payload,
    )
    submitted = submission_response.json()
    if submission_response.status_code != 201 or not submitted.get(
        "reference"
    ):
        raise Exception(
            "Unexpected response from application store when submitting"
            " application: "
            + str(application_id)
            + "application-store-response: "
            + str(submission_response)
            + str(submission_response.json())
        )
    return submitted


@default_bp.errorhandler(404)
def not_found(error):
    current_app.logger.warning(
        f"Encountered 404 against url {request.path}: {error}"
    )
    round_data = get_round_data_fail_gracefully(
        Config.DEFAULT_FUND_ID, Config.DEFAULT_ROUND_ID
    )
    return render_template("404.html", round_data=round_data), 404


@default_bp.errorhandler(500)
@default_bp.errorhandler(Exception)
def internal_server_error(error):
    current_app.logger.error(f"Encountered 500: {error}")
    return render_template("500.html"), 500


@default_bp.errorhandler(401)
def unauthorised_error(error):
    current_app.logger.error(f"Encountered 401: {error}")
    round_data = get_round_data_fail_gracefully(
        Config.DEFAULT_FUND_ID, Config.DEFAULT_ROUND_ID
    )
    return render_template("500.html", round_data=round_data), 401


@default_bp.errorhandler(CSRFError)
@login_requested
def csrf_token_expiry(error):
    if not g.account_id:
        return redirect(g.logout_url)
    current_app.logger.error(f"Encountered 500: {error}")
    return render_template("500.html"), 500
