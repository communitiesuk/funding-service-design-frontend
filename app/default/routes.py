import requests
from app import config
from app.config import APPLICATION_STORE_API_HOST
from app.config import FORM_REHYDRATION_URL
from app.config import FORMS_SERVICE_PUBLIC_HOST
from app.config import SUBMIT_APPLICATION_ENDPOINT
from app.models.application_summary import ApplicationSummary
from app.models.continue_application import continue_form_section
from app.models.eligibility_questions import minimium_money_question_page
from app.models.tasklist import tasklist_page
from app.security.decorator import token_required
from flask import Blueprint
from flask import redirect
from flask import render_template
from flask import request
from flask import url_for

default_bp = Blueprint("routes", __name__, template_folder="templates")


@default_bp.route("/")
def index():
    return render_template(
        "index.html", service_url=url_for("routes.max_funding_criterion")
    )


@default_bp.route("/account/<account_id>")
@token_required
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


@token_required
@default_bp.route("/tasklist/<application_id>", methods=["GET"])
def tasklist(application_id):
    return tasklist_page(application_id)


@default_bp.route("/continue_application/<application_id>", methods=["GET"])
def continue_application(application_id):
    args = request.args
    form_name = args.get("section_name")
    page_name = args.get("page_name")
    continue_form_section(
        application_id, form_name, page_name, FORM_REHYDRATION_URL
    )
    return redirect(f"/tasklist/{application_id}", 302)


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
