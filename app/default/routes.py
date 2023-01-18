from datetime import datetime
from app.default.data import get_fund_data
from app.default.data import get_round_data
from config import Config
from flask import Blueprint
from flask import current_app
from flask import render_template


default_bp = Blueprint("routes", __name__, template_folder="templates")


# TODO Move the following method into utils.
def current_datetime_after_given(value: str) -> bool:
    today = datetime.today().now()
    parsed = datetime.fromisoformat(value)
    return today > parsed


def current_datetime_before_given(value: str) -> bool:
    today = datetime.today().now()
    parsed = datetime.fromisoformat(value)
    return today < parsed



@default_bp.route("/")
def index():
    current_app.logger.info("Service landing page loaded.")
    try:
        round_data = get_round_data(
            Config.DEFAULT_FUND_ID, Config.DEFAULT_ROUND_ID, as_dict=True
        )
        fund_data = get_fund_data(Config.DEFAULT_FUND_ID)
        fund_name = fund_data.get('name')
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
        fund_name = fund_name,
        round_title=round_title,
        submission_deadline=submission_deadline,
        is_past_submission_deadline=current_datetime_after_given(submission_deadline),
        contact_us_email_address=contact_us_email_address,
    )

