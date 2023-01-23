from datetime import datetime
from functools import wraps
from http.client import METHOD_NOT_ALLOWED
import requests
from app.constants import ApplicationStatus
from app.default.data import get_account
from app.default.data import get_application_data
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
from fsd_utils.authentication.decorators import login_required
from flask_babel import force_locale
from app.default.routes import current_datetime_after_given, current_datetime_before_given

application_bp = Blueprint("application_routes", __name__, template_folder="templates")

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

@application_bp.route("/tasklist/<application_id>", methods=["GET"])
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
    round_data = get_round_data(
        Config.DEFAULT_FUND_ID, Config.DEFAULT_ROUND_ID, True
    )

    if current_datetime_before_given(round_data.deadline):
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
                is_past_submission_deadline=current_datetime_after_given(round_data.deadline),
            )
    return redirect(url_for("account_routes.dashboard"))


@application_bp.route("/continue_application/<application_id>", methods=["GET"])
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
        + url_for("application_routes.tasklist", application_id=application_id)[1:]
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


@application_bp.route("/submit_application", methods=["POST"])
@login_required
@verify_application_owner_local
def submit_application():
    round_data = get_round_data_fail_gracefully(
        Config.DEFAULT_FUND_ID, Config.DEFAULT_ROUND_ID)

    if current_datetime_before_given(round_data.deadline):
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
    else:
        return redirect(url_for("routes.dashboard"))


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