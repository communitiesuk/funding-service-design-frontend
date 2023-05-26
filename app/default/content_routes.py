from app.default.data import get_default_fund_and_round
from app.default.data import get_fund_data_by_short_name
from app.default.data import get_round_data_by_short_names
from app.default.data import get_round_data_fail_gracefully
from flask import abort
from flask import Blueprint
from flask import current_app
from flask import redirect
from flask import render_template
from flask import request
from flask import url_for

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

    if fund_short_name.lower() == 'cof':
        if 'r2' in round_short_name.lower():
            return render_template(
                "cof_r2_all_questions.html", round_title=round.title
            )
        elif 'r3' in round_short_name.lower():
            return render_template(
                "cof_r3_all_questions.html", round_title=round.title
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
def contact_us():
    current_app.logger.info("Contact us page loaded.")
    fund_short_name = request.args.get("fund")
    round_short_name = request.args.get("round")
    if not (fund_short_name and round_short_name):
        return render_template("contact_us.html")

    round_data = get_round_data_fail_gracefully(
        fund_short_name, round_short_name, True
    )
    fund_data = get_fund_data_by_short_name(fund_short_name)
    return render_template("contact_us.html",
                           round_data=round_data,
                           fund_name=fund_data.name,)


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
