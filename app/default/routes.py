from app.default.data import get_fund_data
from app.default.data import get_round_data
from config import Config
from flask import Blueprint
from flask import current_app
from flask import render_template
from fsd_utils.simple_utils.date_utils import (
    current_datetime_after_given_iso_string,
)


default_bp = Blueprint("routes", __name__, template_folder="templates")


@default_bp.route("/")
def index():
    current_app.logger.info("Service landing page loaded.")
    default_language = {"language": "en"}
    try:
        round_data = get_round_data(
            fund_id=Config.DEFAULT_FUND_ID, round_id=Config.DEFAULT_ROUND_ID,language=default_language,
            as_dict=True
        )

        fund_data = get_fund_data(
            fund_id=Config.DEFAULT_FUND_ID, language=default_language,
            as_dict=True)
        fund_name = fund_data.name
        submission_deadline = round_data.deadline
        contact_us_email_address = round_data.contact_details["email_address"]
        round_title = round_data.title
    except:  # noqa
        fund_name = ""
        round_title = ""
        submission_deadline = ""
        contact_us_email_address = ""

    return render_template(
        "index.html",
        service_url=Config.ENTER_APPLICATION_URL,
        fund_name=fund_name,
        round_title=round_title,
        submission_deadline=submission_deadline,
        is_past_submission_deadline=current_datetime_after_given_iso_string(
            submission_deadline
        ),
        contact_us_email_address=contact_us_email_address,
    )
