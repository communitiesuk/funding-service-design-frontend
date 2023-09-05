from flask import Blueprint
from flask import current_app
from flask import render_template

content_bp = Blueprint(
    "feedback_routes", __name__, template_folder="templates"
)


@content_bp.route("/section_feedback_intro/<application_id>/<section_id>")
def section_feedback_intro(application_id, section_id):
    current_app.logger.info("Section Feedback Intro page loaded.")
    return render_template("section_feedback_intro.html")
