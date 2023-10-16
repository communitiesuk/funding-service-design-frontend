from app.helpers import find_fund_and_round_in_request
from app.helpers import find_round_in_request
from app.helpers import get_fund_and_round
from flask import abort
from flask import Blueprint
from flask import current_app
from flask import redirect
from flask import render_template
from flask import request
from flask import url_for
from fsd_utils.authentication.decorators import login_requested
from fsd_utils.locale_selector.get_lang import get_lang
from jinja2.exceptions import TemplateNotFound

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
    fund, round = get_fund_and_round(
        fund_short_name=fund_short_name, round_short_name=round_short_name
    )

    if fund and round:
        lang = get_lang()

        # Allow for COF R2 and R3 to use the old mechanism for translating all questions into welsh - the template
        # for these rounds contains translation tags to build the page on the fly.
        # All future rounds that need welsh all questions will have them generated from the form json so should
        # be named with the language in the filename
        all_questions_prefix = (
            f"{fund_short_name.lower()}_{round_short_name.lower()[0:2]}"
        )
        template_name = f"{all_questions_prefix}_all_questions_{lang}.html"
        if fund.welsh_available and all_questions_prefix.startswith(
            ("cof_r2", "cof_r3")
        ):
            template_name = f"{all_questions_prefix}_all_questions.html"
        elif (not fund.welsh_available) and lang != "en":
            template_name = f"{all_questions_prefix}_all_questions_en.html"
        try:
            return render_template(
                template_name,
                fund_title=fund.name,
                round_title=round.title,
            )
        except TemplateNotFound:
            current_app.logger.warn(
                "No all questions page found for"
                f" {fund_short_name}:{round_short_name}"
            )
    return abort(404)


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
    fund, round = find_fund_and_round_in_request()
    fund_name = fund.name if fund else None
    return render_template(
        "contact_us.html",
        round_data=round,
        fund_name=fund_name,
    )


@content_bp.route("/cookie_policy", methods=["GET"])
def cookie_policy():
    current_app.logger.info("Cookie policy page loaded.")
    return render_template("cookie_policy.html")


@content_bp.route("/privacy", methods=["GET"])
def privacy():
    privacy_notice_url = None
    fund, round = find_fund_and_round_in_request()

    privacy_notice_url = (
        getattr(round, "privacy_notice", None) if round else None
    )

    if privacy_notice_url:
        current_app.logger.info(
            f"Privacy notice loading for fund {fund.short_name} round"
            f" {round.short_name}."
        )
        return redirect(privacy_notice_url)

    return abort(404)


@content_bp.route("/feedback", methods=["GET"])
def feedback():
    round = find_round_in_request()
    feedback_url = None

    feedback_url = getattr(round, "feedback_link", None) if round else None

    if feedback_url:
        return redirect(feedback_url)

    return redirect(
        url_for(
            "content_routes.contact_us",
            fund=request.args.get("fund"),
            round=request.args.get("round"),
        )
    )
