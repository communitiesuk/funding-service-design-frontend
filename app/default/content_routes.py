from app.default.data import get_fund_data_by_short_name
from app.default.data import get_round_data_by_short_names
from app.default.data import get_round_data_fail_gracefully
from app.models.round import Round
from flask import abort
from flask import Blueprint
from flask import current_app
from flask import redirect
from flask import render_template
from flask import request
from flask import url_for
from flask import g
from fsd_utils.authentication.decorators import login_requested

content_bp = Blueprint("content_routes", __name__, template_folder="templates")


@content_bp.route("/accessibility_statement", methods=["GET"])
def accessibility_statement():
    current_app.logger.info("Accessibility statement page loaded.")
    return render_template("accessibility_statement.html")


@content_bp.route(
    "/all_questions/<fund_short_name>/<round_short_name>", methods=["GET"]
)
def all_questions(fund_short_name, round_short_name):
    current_app.logger.info(
        f"All questions page loaded for fund {fund_short_name} round"
        f" {round_short_name}."
    )
    round = get_round_data_by_short_names(fund_short_name, round_short_name)
    if not round:
        return abort(404)

    if fund_short_name.lower() == "cof":
        return render_template(
            f"{fund_short_name.lower()}_{round_short_name.lower()[0:2]}_all_questions.html",
            round_title=round.title,
        )


@content_bp.route("/cof_r2w2_all_questions", methods=["GET"])
def cof_r2w2_all_questions_redirect():
    return redirect(
        url_for(
            "content_routes.all_questions",
            fund_short_name="cof",
            round_short_name="r2w2",
        )
    )


@content_bp.route("/contact_us", methods=["GET"])
@login_requested
def contact_us():
    fund_short_name = request.args.get("fund")
    round_short_name = request.args.get("round")
    current_app.logger.info(
        f"Contact us page loaded for fund {fund_short_name} round"
        f" {round_short_name}."
    )
    if round_short_name and fund_short_name:
        round_data = get_round_data_fail_gracefully(
            fund_short_name, round_short_name, True
        )
        fund_data = get_fund_data_by_short_name(fund_short_name)
        fund_name = fund_data.name
    else:
        round_data = Round(
            id="",
            assessment_deadline="",
            deadline="",
            fund_id="",
            opens="",
            title="",
            short_name="",
            prospectus="",
            privacy_notice="",
            instructions="",
            contact_email="",
            contact_phone="",
            contact_textphone="",
            support_days="",
            support_times="",
            feedback_link="",
            project_name_field_id="",
        )
        fund_name = ""
    return render_template(
        "contact_us.html",
        round_data=round_data,
        fund_name=fund_name,
    )


@content_bp.route("/cookie_policy", methods=["GET"])
def cookie_policy():
    current_app.logger.info("Cookie policy page loaded.")
    return render_template("cookie_policy.html")


@content_bp.route("/privacy", methods=["GET"])
def privacy():
    current_app.logger.info("Privacy_notice page loaded.")
    fund_short_name = request.args.get("fund")
    round_short_name = request.args.get("round")
    if fund_short_name and round_short_name:
        round_data = get_round_data_by_short_names(
            fund_short_name, round_short_name
        )
        privacy_notice_url = getattr(round_data, "privacy_notice", None)

        if privacy_notice_url:
            current_app.logger.info("Privacy notice configured for fund")
            return redirect(privacy_notice_url)

    current_app.logger.warning(
        f"No privacy notice configured for round ({fund_short_name} -"
        f" {round_short_name}). Redirecting..."
    )
    return redirect(
        "https://www.gov.uk/government/publications/community-ownership-fund-privacy-notice/community-ownership-fund-privacy-notice"  # noqa
    )


@content_bp.route("/feedback", methods=["GET"])
def feedback():
    fund_short_name = request.args.get("fund")
    round_short_name = request.args.get("round")
    current_app.logger.info(
        f"Feedback page loading for fund {fund_short_name} round"
        f" {round_short_name}."
    )
    if fund_short_name and round_short_name:
        round_data = get_round_data_by_short_names(
            fund_short_name, round_short_name
        )
        feedback_url = getattr(round_data, "feedback_link", None)

        if feedback_url:
            current_app.logger.debug("Feedback link configured for fund")
            return redirect(feedback_url)

    current_app.logger.warning(
        f"No feedback url configured for round ({fund_short_name} -"
        f" {round_short_name}). Redirecting..."
    )
    return redirect(
        url_for(
            "content_routes.contact_us",
            fund=fund_short_name,
            round=round_short_name,
        )
    )
