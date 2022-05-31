import requests
from app import config
from app.config import APPLICATION_STORE_API_HOST
from app.config import FORM_REHYDRATION_URL
from app.config import FORMS_SERVICE_PUBLIC_HOST
from app.config import SUBMIT_APPLICATION_ENDPOINT
from app.default.data import get_application_data
from app.models.application import Application
from app.models.application_summary import ApplicationSummary
from app.models.eligibility_questions import minimium_money_question_page
from app.models.helpers import format_rehydrate_payload
from app.models.helpers import get_token_to_return_to_application
from flask import abort
from flask import Blueprint
from flask import redirect
from flask import render_template
from flask import request
from flask import url_for
from flask_wtf import FlaskForm


default_bp = Blueprint("routes", __name__, template_folder="templates")


@default_bp.route("/")
def index():
    return render_template(
        "index.html", service_url=url_for("routes.max_funding_criterion")
    )


@default_bp.route("/account/<account_id>")
def dashboard(account_id):
    response = requests.get(
        f"{APPLICATION_STORE_API_HOST}/applications?account_id={account_id}"
    ).json()
    applications: list[ApplicationSummary] = [
        ApplicationSummary.from_dict(application) for application in response
    ]
    if len(applications) > 0:
        round_id = applications[0].round_id
        fund_id = applications[0].fund_id
    else:
        round_id = config.DEFAULT_ROUND_ID
        fund_id = config.DEFAULT_FUND_ID
    return render_template(
        "dashboard.html",
        account_id=account_id,
        applications=applications,
        round_id=round_id,
        fund_id=fund_id,
    )


@default_bp.route("/account/<account_id>/new", methods=["POST"])
def new(account_id):
    new_application = requests.post(
        url=f"{APPLICATION_STORE_API_HOST}/applications",
        json={
            "account_id": account_id,
            "round_id": request.form["round_id"] or config.DEFAULT_ROUND_ID,
            "fund_id": request.form["fund_id"] or config.DEFAULT_FUND_ID,
        },
    )
    new_application_json = new_application.json()
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


@default_bp.route("/funding_amount_eligibility", methods=["GET", "POST"])
def max_funding_criterion():
    return minimium_money_question_page(1000, FORMS_SERVICE_PUBLIC_HOST)


@default_bp.route("/not-eligible")
def not_eligible():
    return render_template("not_eligible.html")


@default_bp.route("/tasklist/<application_id>", methods=["GET"])
def tasklist(application_id):
    """
    Returns a Flask function which constructs a tasklist for an application id.

    Args:
        application_id (str): the id of an application in the application store

    Returns:
        function: a function which renders the tasklist template.
    """
    application_response = get_application_data(application_id)
    if not (application_response and application_response["sections"]):
        return abort(404)
    application = Application.from_dict(application_response)
    form = FlaskForm()
    application_meta_data = {
        "application_id": application_id,
        "round": application.round_id,
        "fund": application.fund_id,
        "number_of_sections": len(application.sections),
        "number_of_completed_sections": len(
            list(
                filter(
                    lambda section: section["status"] == "SUBMITTED",
                    application.sections,
                )
            )
        ),
        "number_of_incomplete_sections": len(
            list(
                filter(
                    lambda section: section["status"] == "NOT_STARTED",
                    application.sections,
                )
            )
        ),
    }
    return render_template(
        "tasklist.html",
        application_response=application,
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
        form_name (str): The name of the application sub form/section
        page_name (str): The form page to redirect the user to.

    Returns:
        A function: given a users application id they are redirected to
        the specified application form page within the form runner service
    """
    args = request.args
    form_name = args.get("section_name")
    page_name = args.get("page_name")

    response = get_application_data(application_id)
    application_data = Application.from_dict(response)
    section = application_data.get_section_data(application_data, form_name)

    rehydrate_payload = format_rehydrate_payload(
        section, application_id, page_name
    )

    rehydration_token = get_token_to_return_to_application(
        form_name, rehydrate_payload
    )

    return redirect(
        FORM_REHYDRATION_URL.format(rehydration_token=rehydration_token)
    )


@default_bp.route("/submit_application", methods=["POST"])
def submit_application():
    application_id = request.form.get("application_id")
    payload = {"application_id": application_id}
    requests.post(
        SUBMIT_APPLICATION_ENDPOINT.format(application_id=application_id),
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
