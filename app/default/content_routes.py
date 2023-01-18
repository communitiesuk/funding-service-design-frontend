
from flask import Blueprint
from flask import current_app
from config import Config
from app.default.data import get_round_data_fail_gracefully
from flask import render_template

content_bp = Blueprint("content_routes", __name__, template_folder="templates")

@content_bp.route("/accessibility_statement", methods=["GET"])
def accessibility_statement():
    current_app.logger.info("Accessibility statement page loaded.")
    return render_template("accessibility_statement.html")


@content_bp.route("/cof_r2w2_all_questions", methods=["GET"])
def all_questions():
    current_app.logger.info("All questions page loaded.")
    return render_template("cof_r2w2_all_questions.html")


@content_bp.route("/contact_us", methods=["GET"])
def contact_us():
    current_app.logger.info("Contact us page loaded.")
    round_data = get_round_data_fail_gracefully(
        Config.DEFAULT_FUND_ID, Config.DEFAULT_ROUND_ID
    )
    return render_template("contact_us.html", round_data=round_data)


@content_bp.route("/cookie_policy", methods=["GET"])
def cookie_policy():
    current_app.logger.info("Cookie policy page loaded.")
    return render_template("cookie_policy.html")