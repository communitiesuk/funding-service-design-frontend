import requests
from app.default.data import get_all_funds
from app.default.data import get_all_rounds_for_fund
from app.default.data import get_applications_for_account
from app.models.application_summary import ApplicationSummary
from config import Config
from flask import Blueprint
from flask import current_app
from flask import g
from flask import redirect
from flask import render_template
from flask import request
from flask import url_for
from fsd_utils.authentication.decorators import login_required
from fsd_utils.locale_selector.get_lang import get_lang
from fsd_utils.simple_utils.date_utils import (
    current_datetime_after_given_iso_string,
)
from fsd_utils.simple_utils.date_utils import (
    current_datetime_before_given_iso_string,
)


account_bp = Blueprint("account_routes", __name__, template_folder="templates")


def build_application_data_for_display(applications: list[ApplicationSummary]):

    application_data_for_display = {}

    all_funds = get_all_funds()
    for fund in all_funds:
        fund_id = fund["id"]
        all_rounds_in_fund = get_all_rounds_for_fund()
        application_data_for_display[fund_id] = {
            "fund_data": fund,
            "rounds": [],
        }
        for round in all_rounds_in_fund:
            round_id = round["id"]
            past_submission_deadline = current_datetime_after_given_iso_string(
                round["deadline"]
            )
            not_yet_open = current_datetime_before_given_iso_string(
                round["opens"]
            )
            apps_in_this_round = [
                app for app in applications if app.round_id == round_id
            ]
            application_data_for_display[fund_id]["rounds"].append(
                {
                    "is_past_submission_deadline": past_submission_deadline,
                    "is_not_yet_open": not_yet_open,
                    "round_details": round,
                    "applications": apps_in_this_round,
                }
            )

            for application in apps_in_this_round:
                if past_submission_deadline:
                    if application.status != "SUBMITTED":
                        application.status = "NOT_SUBMITTED"
                else:
                    if application.status == "COMPLETED":
                        application.status = "READY_TO_SUBMIT"

        return application_data_for_display


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
    # rounds_with_applications = [app['round_id'] for app in applications]

    display_data = build_application_data_for_display(applications)

    # # build data for each round we need
    # if len(rounds_with_applications) > 0:
    #     for round in rounds_with_applications
    # else:
    #     round_data_for_display[Config.DEFAULT_ROUND_ID]:
    #     build_round_data_for_display(Config.DEFAULT_FUND_ID,
    #     Config.DEFAULT_ROUND_ID)

    # if len(applications) > 0:
    #     round_id = applications[0].round_id
    #     fund_id = applications[0].fund_id
    # else:
    #     round_id = Config.DEFAULT_ROUND_ID
    #     fund_id = Config.DEFAULT_FUND_ID

    # round_data = get_round_data_fail_gracefully(
    # Config.DEFAULT_FUND_ID, Config.DEFAULT_ROUND_ID)

    # current_app.logger.info(
    #     f"Setting up applicant dashboard for :'{account_id}'
    #     to apply for fund"
    #     f" {fund_id} on round {round_id}"
    # )

    return render_template(
        "dashboard.html",
        account_id=account_id,
        display_data=display_data,
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
            "application_routes.tasklist",
            application_id=new_application.json().get("id"),
        )
    )
