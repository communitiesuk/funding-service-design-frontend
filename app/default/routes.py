from app.forms.eligibility_questions import minimium_money_question_page
from flask import Blueprint
from flask import render_template
from flask import url_for

default_bp = Blueprint("routes", __name__, template_folder="templates")


@default_bp.route("/")
def index():
    return render_template(
        "index.html", service_url=url_for("routes.max_funding_criterion")
    )


@default_bp.route("/funding_amount_eligibility", methods=["GET", "POST"])
def max_funding_criterion():
    return minimium_money_question_page(
        1000,
        "https://funding-service-design-form-runner."
        "london.cloudapps.digital/funding-application"
        "/about-you",
    )

@default_bp.route("/not-eligible")
def not_eligible():
    return render_template(
    "not_eligible.html"
    )

@default_bp.errorhandler(404)
def not_found(error):
    return render_template("404.html"), 404


@default_bp.errorhandler(500)
def internal_server_error(error):
    return render_template("500.html"), 500
