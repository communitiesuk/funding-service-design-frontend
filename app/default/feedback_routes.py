from app.helpers import find_fund_and_round_in_request
from app.helpers import find_round_in_request
from app.helpers import get_round
from flask import abort
from flask import Blueprint
from flask import current_app
from flask import redirect
from flask import render_template
from flask import request
from flask import url_for
from fsd_utils.authentication.decorators import login_requested

content_bp = Blueprint(
    "feedback_routes", __name__, template_folder="templates"
)


@content_bp.route("/section_feedback_intro/<application_id>/<section_id>")
def section_feedback_intro(application_id, section_id):
    current_app.logger.info("Section Feedback Intro page loaded.")
    return render_template("section_feedback_intro.html")
