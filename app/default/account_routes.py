
import requests
from app.default.data import get_applications_for_account
from app.default.data import get_round_data_fail_gracefully
from flask import request
from flask import url_for
from fsd_utils.authentication.decorators import login_required
from fsd_utils.locale_selector.get_lang import get_lang
from app.models.application_summary import ApplicationSummary
from flask import current_app
from config import Config
from flask import Blueprint, g, redirect, render_template
from app.default.routes import current_datetime_after_given, current_datetime_before_given


account_bp = Blueprint("account_routes", __name__, template_folder="templates")

@account_bp.route("/account")
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

    round_data = get_round_data_fail_gracefully(
    Config.DEFAULT_FUND_ID, Config.DEFAULT_ROUND_ID)

    current_app.logger.info(
        f"Setting up applicant dashboard for :'{account_id}' to apply for fund"
        f" {fund_id} on round {round_id}"
    )

    if current_datetime_before_given(round_data.deadline):
        for application in applications:
            if application.status == "COMPLETED":
                application.status = "READY_TO_SUBMIT"

    if current_datetime_after_given(round_data.deadline):
        for application in applications:
            if application.status != "SUBMITTED":
                application.status = "NOT_SUBMITTED"

    return render_template(
            "dashboard.html",
            account_id=account_id,
            applications=applications,
            round_id=round_id,
            fund_id=fund_id,
            submission_deadline=round_data.deadline,
            is_past_submission_deadline=current_datetime_after_given(round_data.deadline),
            round_title=round_data.title,
            fund_name="Community Ownership Fund",
        )


@account_bp.route("/account/new", methods=["POST"])
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
            "application_routes.tasklist", application_id=new_application.json().get("id")
        )
    )