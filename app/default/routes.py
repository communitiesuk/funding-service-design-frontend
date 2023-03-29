from app.default.data import determine_round_status
from app.default.data import get_fund_data
from app.default.data import get_fund_data_by_short_name
from app.default.data import get_round_data
from app.default.data import get_round_data_by_short_names
from config import Config
from flask import abort
from flask import Blueprint
from flask import current_app
from flask import render_template
from fsd_utils.simple_utils.date_utils import (
    current_datetime_after_given_iso_string,
)

default_bp = Blueprint("routes", __name__, template_folder="templates")


# TODO Do not change this until after COF R2 W3 closes as this
# provides the current landing page!
@default_bp.route("/")
def index():
    current_app.logger.info("Service landing page loaded.")
    try:
        round_data = get_round_data(
            fund_id=Config.DEFAULT_FUND_ID,
            round_id=Config.DEFAULT_ROUND_ID,
            as_dict=False,
        )

        fund_data = get_fund_data(fund_id=Config.DEFAULT_FUND_ID, as_dict=True)
        fund_name = fund_data.name
        submission_deadline = round_data.deadline
        contact_us_email_address = round_data.contact_details["email_address"]
        round_title = round_data.title
        is_past_submission_deadline = current_datetime_after_given_iso_string(
            submission_deadline
        )
    except Exception as e:  # noqa
        current_app.log_exception(e)
        fund_name = ""
        round_title = ""
        submission_deadline = ""
        contact_us_email_address = ""
        is_past_submission_deadline = False

    return render_template(
        "index.html",
        service_url=Config.ENTER_APPLICATION_URL,
        fund_name=fund_name,
        round_title=round_title,
        submission_deadline=submission_deadline,
        is_past_submission_deadline=is_past_submission_deadline,
        contact_us_email_address=contact_us_email_address,
    )


@default_bp.route("/<fund_short_name>/<round_short_name>")
def index_fund_round(fund_short_name, round_short_name):
    current_app.logger.info(
        f"In fund-round start page {fund_short_name} {round_short_name}"
    )
    fund_data = get_fund_data_by_short_name(fund_short_name, as_dict=False)
    if not fund_data:
        abort(404)
    round_data = get_round_data_by_short_names(
        fund_short_name, round_short_name
    )
    if not round_data:
        abort(404)
    round_status = determine_round_status(round_data)
    if round_status.not_yet_open:
        abort(404)

    return render_template(
        "fund_start_page.html",
        service_url=Config.MAGIC_LINK_URL.format(
            fund_short_name=fund_short_name, round_short_name=round_short_name
        ),
        fund_name=fund_data.name,
        fund_title=fund_data.title,
        round_title=round_data.title,
        submission_deadline=round_data.deadline,
        is_past_submission_deadline=round_status.past_submission_deadline,
        contact_us_email_address=round_data.contact_details["email_address"],
        prospectus_link=round_data.prospectus,
        instruction_text=round_data.instructions,
    )
