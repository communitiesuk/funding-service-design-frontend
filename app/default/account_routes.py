import requests
from app.default.data import determine_round_status
from app.default.data import get_all_funds
from app.default.data import get_all_rounds_for_fund
from app.default.data import get_applications_for_account
from app.default.data import get_round_data_by_short_names
from app.default.data import search_applications
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
from fsd_utils.authentication.decorators import login_required
from fsd_utils.locale_selector.get_lang import get_lang


account_bp = Blueprint("account_routes", __name__, template_folder="templates")


def build_application_data_for_display(
    applications: list[ApplicationSummary], visible_fund_short_name
):

    application_data_for_display = {
        "funds": [],
        "total_applications_to_display": 0,
    }

    funds_to_show = get_all_funds()
    if not funds_to_show:
        return application_data_for_display
    count_of_applications_for_visible_rounds = 0

    if visible_fund_short_name:
        try:
            funds_to_show = [
                fund
                for fund in funds_to_show
                if fund["short_name"].casefold()
                == visible_fund_short_name.casefold()
            ]
        except StopIteration:
            return abort(404)
    for fund in funds_to_show:
        fund_id = fund["id"]
        all_rounds_in_fund = get_all_rounds_for_fund(fund_id, as_dict=False)
        fund_data_for_display = {
            "fund_data": fund,
            "rounds": [],
        }
        for round in all_rounds_in_fund:
            round_id = round.id
            round_status = determine_round_status(round)
            apps_in_this_round = [
                app for app in applications if app.round_id == round_id
            ]
            if round_status.not_yet_open or (
                round_status.past_submission_deadline
                and len(apps_in_this_round) == 0
            ):
                continue
            for application in apps_in_this_round:
                if round_status.past_submission_deadline:
                    if application.status != "SUBMITTED":
                        application.status = "NOT_SUBMITTED"
                else:
                    if application.status == "COMPLETED":
                        application.status = "READY_TO_SUBMIT"
            fund_data_for_display["rounds"].append(
                {
                    "is_past_submission_deadline": round_status.past_submission_deadline,  # noqa
                    "is_not_yet_open": round_status.not_yet_open,
                    "round_details": round,
                    "applications": apps_in_this_round,
                }
            )
            count_of_applications_for_visible_rounds += len(apps_in_this_round)
        fund_data_for_display["rounds"] = sorted(
            fund_data_for_display["rounds"],
            key=lambda r: r["round_details"].opens,
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

    fund_short_name = request.args.get("fund")
    round_short_name = request.args.get("round")

    if fund_short_name and round_short_name:
        # search for applications for this account AND
        # this fund if fund is supplied, else get all
        # applications for this account
        round_details = get_round_data_by_short_names(
            fund_short_name,
            round_short_name,
        )
        application_store_response = search_applications(
            search_params={
                "fund_id": round_details.fund_id,
                "round_id": round_details.id,
                "account_id": account_id,
            },
            as_dict=True,
        )
    else:
        # Generic all applications dashboard
        application_store_response = get_applications_for_account(
            account_id=account_id, as_dict=True
        )

    applications: list[ApplicationSummary] = [
        ApplicationSummary.from_dict(application)
        for application in application_store_response
    ]

    show_language_column = len({a.language for a in applications}) > 1

    display_data = build_application_data_for_display(
        applications, fund_short_name
    )
    current_app.logger.info(
        f"Setting up applicant dashboard for :'{account_id}'"
    )
    # TODO will need to tell the dashboard template whether it's for a
    # particular fund or it's the generic dashboard.
    return render_template(
        "dashboard.html",
        account_id=account_id,
        display_data=display_data,
        show_language_column=show_language_column,
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
