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

    application_data_for_display = {
        "funds": [],
        "total_applications_to_display": 0,
    }

    all_funds = get_all_funds()
    if not all_funds:
        return application_data_for_display
    count_of_applications_for_visible_rounds = 0

    for fund in all_funds:
        fund_id = fund["id"]
        all_rounds_in_fund = get_all_rounds_for_fund(fund_id)
        fund_data_for_display = {
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
            if not_yet_open or (
                past_submission_deadline and len(apps_in_this_round) == 0
            ):
                continue
            for application in apps_in_this_round:
                if past_submission_deadline:
                    if application.status != "SUBMITTED":
                        application.status = "NOT_SUBMITTED"
                else:
                    if application.status == "COMPLETED":
                        application.status = "READY_TO_SUBMIT"
            fund_data_for_display["rounds"].append(
                {
                    "is_past_submission_deadline": past_submission_deadline,
                    "is_not_yet_open": not_yet_open,
                    "round_details": round,
                    "applications": apps_in_this_round,
                }
            )
            count_of_applications_for_visible_rounds += len(apps_in_this_round)
        fund_data_for_display["rounds"] = sorted(
            fund_data_for_display["rounds"],
            key=lambda r: r["round_details"]["opens"],
            reverse=True,
        )

        application_data_for_display["funds"].append(fund_data_for_display)

    application_data_for_display[
        "total_applications_to_display"
    ] = count_of_applications_for_visible_rounds
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

    showLanguageColumn = len({a.language for a in applications}) > 1

    display_data = build_application_data_for_display(applications)
    current_app.logger.info(
        f"Setting up applicant dashboard for :'{account_id}'"
    )
    return render_template(
        "dashboard.html",
        account_id=account_id,
        display_data=display_data,
        showLanguageColumn=showLanguageColumn
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
