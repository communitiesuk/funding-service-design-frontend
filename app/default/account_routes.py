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
        all_rounds_in_fund = get_all_rounds_for_fund(fund_id)
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
            if not not_yet_open:
                application_data_for_display[fund_id]["rounds"].append(
                    {
                        "is_past_submission_deadline": past_submission_deadline,  # noqa:E501
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
# @login_required
def dashboard():
    account_id = "test-user"  # g.account_id
    application_store_response = get_applications_for_account(
        account_id=account_id, as_dict=False
    )

    # application_store_response = [
    #     {
    #         "id": "uuidv4",
    #         "status": "IN_PROGRESS",
    #         "account_id": "test-user",
    #         "fund_id": "funding-service-design",
    #         "round_id": "summer",
    #         "reference": "TEST-REF-B",
    #         "project_name": None,
    #         "date_submitted": None,
    #         "started_at": "2022-05-20 14:47:12",
    #         "last_edited": "2022-05-24 11:03:59",
    #         "language": "en",
    #     },
    #     {
    #         "id": "ed221ac8-5d4d-42dd-ab66-6cbcca8fe257",
    #         "status": "COMPLETED",
    #         "account_id": "test-user",
    #         "fund_id": "funding-service-design",
    #         "round_id": "summer",
    #         "reference": "TEST-REF-C",
    #         "project_name": "",
    #         "date_submitted": None,
    #         "started_at": "2022-05-24 10:42:41",
    #         "last_edited": None,
    #         "language": "en",
    #         "Unknown": "DOES NOT MAKE ME FAIL",
    #     },
    #     {
    #         "id": "ed221ac8-5d4d-42dd-ab66-6cbcca8fe257",
    #         "status": "IN_PROGRESS",
    #         "account_id": "test-user",
    #         "fund_id": "funding-service-design",
    #         "round_id": "cof-r2w2",
    #         "reference": "TEST-REF-C",
    #         "project_name": "cool project from w2",
    #         "date_submitted": None,
    #         "started_at": "2022-05-24 10:42:41",
    #         "last_edited": None,
    #         "language": "en",
    #         "Unknown": "DOES NOT MAKE ME FAIL",
    #     },
    # ]

    applications: list[ApplicationSummary] = [
        ApplicationSummary.from_dict(application)
        for application in application_store_response
    ]

    # display_data = {
    #     "funding-service-design": {
    #         "fund_data": {
    #             "id": "funding-service-design",
    #             "name": "Test Fund",
    #             "description": "test test",
    #             "short_name": "FSD",
    #         },
    #         "rounds": [
    #             {
    #                 "is_past_submission_deadline": True,
    #                 "is_not_yet_open": False,
    #                 "round_details": {
    #                     "opens": "2022-09-01 00:00:01",
    #                     "deadline": "2030-01-30 00:00:01",
    #                     "assessment_deadline": "2030-03-20 00:00:01",
    #                     "id": "cof-r2w2",
    #                     "title": "Round 2 Window 2",
    #                     "fund_id": "fund-service-design",
    #                     "short_name": "R2W2",
    #                     "assessment_criteria_weighting": [],
    #                     "contact_details": {},
    #                     "support_availability": {},
    #                 },
    #                 "applications": [
    #                     {
    #                         "id": "uuidv4",
    #                         "reference": "TEST-REF-B",
    #                         "status": "NOT_SUBMITTED",
    #                         "round_id": "summer",
    #                         "fund_id": "funding-service-design",
    #                         "started_at": "2020-01-01 12:03:00",
    #                         "project_name": None,
    #                         "last_edited": "2020-01-01 12:03:00",
    #                     },
    #                     {
    #                         "id": "ed221ac8-5d4d-42dd-ab66-6cbcca8fe257",
    #                         "reference": "TEST-REF-C",
    #                         "status": "SUBMITTED",
    #                         "round_id": "summer",
    #                         "fund_id": "funding-service-design",
    #                         "started_at": "2023-01-01 12:01:00",
    #                         "project_name": "",
    #                         "last_edited": None,
    #                     },
    #                 ],
    #             },
    #             {
    #                 "is_past_submission_deadline": False,
    #                 "is_not_yet_open": False,
    #                 "round_details": {
    #                     "opens": "2022-09-01 00:00:01",
    #                     "deadline": "2030-01-30 00:00:01",
    #                     "assessment_deadline": "2030-03-20 00:00:01",
    #                     "id": "summer",
    #                     "title": "Summer round",
    #                     "fund_id": "fund-service-design",
    #                     "short_name": "R2W3",
    #                     "assessment_criteria_weighting": [],
    #                     "contact_details": {},
    #                     "support_availability": {},
    #                 },
    #                 "applications": [
    #                     {
    #                         "id": "uuidv4",
    #                         "reference": "TEST-REF-B",
    #                         "status": "IN_PROGRESS",
    #                         "round_id": "summer",
    #                         "fund_id": "funding-service-design",
    #                         "started_at": "2020-01-01 12:03:00",
    #                         "project_name": None,
    #                         "last_edited": "2020-01-01 12:03:00",
    #                     },
    #                     {
    #                         "id": "ed221ac8-5d4d-42dd-ab66-6cbcca8fe257",
    #                         "reference": "TEST-REF-C",
    #                         "status": "READY_TO_SUBMIT",
    #                         "round_id": "summer",
    #                         "fund_id": "funding-service-design",
    #                         "started_at": "2023-01-01 12:01:00",
    #                         "project_name": "",
    #                         "last_edited": None,
    #                     },
    #                 ],
    #             },
    #             {
    #                 "is_past_submission_deadline": False,
    #                 "is_not_yet_open": True,
    #                 "round_details": {
    #                     "opens": "2022-09-01 00:00:01",
    #                     "deadline": "2030-01-30 00:00:01",
    #                     "assessment_deadline": "2030-03-20 00:00:01",
    #                     "id": "future",
    #                     "title": "Future round",
    #                     "fund_id": "fund-service-design",
    #                     "short_name": "R2W222",
    #                     "assessment_criteria_weighting": [],
    #                     "contact_details": {},
    #                     "support_availability": {},
    #                 },
    #                 "applications": [],
    #             },
    #         ],
    #     }
    # }
    display_data = build_application_data_for_display(applications)
    current_app.logger.info(
        f"Setting up applicant dashboard for :'{account_id}'"
    )
    return render_template(
        "dashboard.html",
        account_id=account_id,
        funds=display_data,
        total_applications_all_rounds=len(applications),
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
