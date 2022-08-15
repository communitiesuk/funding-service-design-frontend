import requests
from app.application_status import ApplicationStatus
from app.default.data import get_application_data
from app.default.data import get_data
from app.default.data import get_fund_data
from app.models.application_summary import ApplicationSummary
from app.models.helpers import format_rehydrate_payload
from app.models.helpers import get_token_to_return_to_application
from config import Config
from flask import Blueprint
from flask import current_app
from flask import redirect
from flask import render_template
from flask import request
from flask import url_for
from flask_wtf import FlaskForm
from fsd_utils.authentication.decorators import login_required


default_bp = Blueprint("routes", __name__, template_folder="templates")


@default_bp.route("/")
def index():
    current_app.logger.info("Service landing page loaded.")
    return render_template(
        "index.html", service_url=Config.ENTER_APPLICATION_URL
    )


@default_bp.route("/accessibility_statement", methods=["GET"])
def accessibility_statement():
    current_app.logger.info("Accessibility statement page loaded.")
    return render_template("accessibility-statement.html")


@default_bp.route("/cookie_policy", methods=["GET"])
def cookie_policy():
    current_app.logger.info("Cookie policy page loaded.")
    return render_template("cookie_policy.html")


@default_bp.route("/account")
@login_required
def dashboard(account_id):
    response = get_data(
        Config.GET_APPLICATIONS_FOR_ACCOUNT_ENDPOINT.format(
            account_id=account_id
        )
    )
    applications: list[ApplicationSummary] = [
        ApplicationSummary.from_dict(application) for application in response
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

    return render_template(
        "dashboard.html",
        account_id=account_id,
        applications=applications,
        round_id=round_id,
        fund_id=fund_id,
    )


@default_bp.route("/account/new", methods=["POST"])
@login_required
def new(account_id):
    new_application = requests.post(
        url=f"{Config.APPLICATION_STORE_API_HOST}/applications",
        json={
            "account_id": account_id,
            "round_id": request.form["round_id"] or Config.DEFAULT_ROUND_ID,
            "fund_id": request.form["fund_id"] or Config.DEFAULT_FUND_ID,
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
def tasklist(application_id):
    """
    Returns a Flask function which constructs a tasklist for an application id.

    Args:
        application_id (str): the id of an application in the application store

    Returns:
        function: a function which renders the tasklist template.
    """

    application = get_application_data(application_id, as_dict=True)
    fund = get_fund_data(application.fund_id, as_dict=True)
    application.create_sections(application)

    form = FlaskForm()
    application_meta_data = {
        "application_id": application_id,
        "fund_name": fund.name,
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
    return render_template(
        "tasklist.html",
        application=application,
        application_meta_data=application_meta_data,
        form=form,
    )


@default_bp.route("/continue_application/<application_id>", methods=["GET"])
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
def submit_application():
    application_id = request.form.get("application_id")
    payload = {"application_id": application_id}
    requests.post(
        Config.SUBMIT_APPLICATION_ENDPOINT.format(
            application_id=application_id
        ),
        json=payload,
    )
    return render_template(
        "application_submitted.html", application_id=application_id
    )


@default_bp.errorhandler(404)
def not_found(error):
    return render_template("404.html"), 404


@default_bp.errorhandler(500)
def internal_server_error(error):
    return render_template("500.html"), 500
