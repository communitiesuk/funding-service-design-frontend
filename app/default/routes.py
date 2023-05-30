from app.default.data import determine_round_status
from app.default.data import get_default_round_for_fund
from app.default.data import get_fund_data_by_short_name
from app.default.data import get_round_data_by_short_names
from app.models.fund import FUND_SHORT_CODES
from app.models.round import Round
from config import Config
from flask import abort
from flask import Blueprint
from flask import current_app
from flask import redirect
from flask import render_template

default_bp = Blueprint("routes", __name__, template_folder="templates")


@default_bp.route("/")
def index():
    """
    Redirects from the old landing page to the new one at /cof/r2w3
    """
    return abort(404)


@default_bp.route("/funding-round/<fund_short_name>/<round_short_name>")
def index_fund_round(fund_short_name, round_short_name):
    current_app.logger.info(
        f"In fund-round start page {fund_short_name} {round_short_name}"
    )
    fund_data = get_fund_data_by_short_name(fund_short_name, as_dict=False)
    round_data = get_round_data_by_short_names(
        fund_short_name, round_short_name
    )
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
        contact_us_email_address=round_data.contact_email,
        prospectus_link=round_data.prospectus,
        instruction_text=round_data.instructions,
    )


@default_bp.route("/funding-round/<fund_short_name>")
def index_fund_only(fund_short_name):
    if str.upper(fund_short_name) in [
        member.value for member in FUND_SHORT_CODES
    ]:
        current_app.logger.info(
            f"In fund-only start page route for {fund_short_name}"
        )
        default_round = get_default_round_for_fund(
            fund_short_name=fund_short_name
        )
        if default_round:
            return redirect(
                f"/funding-round/{fund_short_name}/{default_round.short_name}"
            )

        current_app.logger.warn(
            f"Unable to retrieve default round for fund {fund_short_name}"
        )
    return (
        render_template(
            "404.html",
            round_data=Round("", [], "", "", "", "", "", "", "", "", {}, {}),
        ),
        404,
    )
