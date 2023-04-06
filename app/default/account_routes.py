import requests
from app.default.data import determine_round_status
from app.default.data import get_all_funds
from app.default.data import get_all_rounds_for_fund
from app.default.data import get_round_data_by_short_names
from app.default.data import RoundStatus
from app.default.data import search_applications
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


account_bp = Blueprint("account_routes", __name__, template_folder="templates")


def get_visible_funds(visible_fund_short_name):
    """
    Returns a list of funds matching the supplied short name

    :param visible_fund_short_name: short name to look for
    """
    all_funds = get_all_funds()

    if visible_fund_short_name:
        funds_to_show = [
            fund
            for fund in all_funds
            if fund["short_name"].casefold()
            == visible_fund_short_name.casefold()
        ]
    else:
        funds_to_show = all_funds

    if not funds_to_show or len(funds_to_show) == 0:
        return []
    else:
        return funds_to_show


def update_applications_statuses_for_display(
    applications: list[ApplicationSummary], round_status: RoundStatus
) -> list[ApplicationSummary]:
    """
    Updates the status value of each application in the supplied list
    to work for display:
    If the round is closed, all un-submitted applications get a status
    of NOT_SUBMITTED.
    If the round is open, any COMPLETED applications are updated to
    READY_TO_SUBMIT

    :param applications: List of applications to update statuses for
    :param round_status: Round status object, used in determining the
    display status
    """
    for application in applications:
        if round_status.past_submission_deadline:
            if application.status != "SUBMITTED":
                application.status = "NOT_SUBMITTED"
        else:
            if application.status == "COMPLETED":
                application.status = "READY_TO_SUBMIT"
    return applications


def build_application_data_for_display(
    applications: list[ApplicationSummary], visible_fund_short_name
):
    application_data_for_display = {
        "funds": [],
        "total_applications_to_display": 0,
    }
    count_of_applications_for_visible_rounds = 0

    funds_to_show = get_visible_funds(visible_fund_short_name)
    for fund in funds_to_show:
        fund_id = fund["id"]
        all_rounds_in_fund = get_all_rounds_for_fund(fund_id, as_dict=False)
        fund_data_for_display = {
            "fund_data": fund,
            "rounds": [],
        }
        for round in all_rounds_in_fund:
            round_status = determine_round_status(round)
            apps_in_this_round = [
                app for app in applications if app.round_id == round.id
            ]
            if round_status.not_yet_open or (
                round_status.past_submission_deadline
                and len(apps_in_this_round) == 0
            ):
                continue
            apps_for_display = update_applications_statuses_for_display(
                apps_in_this_round, round_status
            )
            fund_data_for_display["rounds"].append(
                {
                    "is_past_submission_deadline": round_status.past_submission_deadline,  # noqa
                    "is_not_yet_open": round_status.not_yet_open,
                    "round_details": round,
                    "applications": apps_for_display,
                }
            )
            count_of_applications_for_visible_rounds += len(apps_for_display)
        if len(fund_data_for_display["rounds"]) == 0:
            continue
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


def determine_show_language_column(applications):
    """
    Determine whether the language column should be visible -
    true if applications are in more than one language
    """
    return len({a.language for a in applications}) > 1


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
        search_params = {
            "fund_id": round_details.fund_id,
            "round_id": round_details.id,
            "account_id": account_id,
        }
    else:
        # Generic all applications dashboard
        search_params = {"account_id": account_id}

    applications = search_applications(
        search_params=search_params, as_dict=False
    )

    # applications: list[ApplicationSummary] = [
    #     ApplicationSummary.from_dict(application)
    #     for application in application_store_response
    # ]

    show_language_column = determine_show_language_column(applications)

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
