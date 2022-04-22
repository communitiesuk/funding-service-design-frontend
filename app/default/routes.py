from app.config import FORMS_SERVICE_PUBLIC_HOST
from app.default.data import format_application_data
from app.default.data import get_application_data
from app.default.helpers import get_return_to_runner_token
from app.forms.eligibility_questions import minimium_money_question_page
from flask import Blueprint
from flask import redirect
from flask import render_template
from flask import request
from flask import url_for
from flask_wtf import FlaskForm

default_bp = Blueprint("routes", __name__, template_folder="templates")


@default_bp.route("/")
def index():
    return render_template(
        "index.html", service_url=url_for("routes.max_funding_criterion")
    )


@default_bp.route("/funding_amount_eligibility", methods=["GET", "POST"])
def max_funding_criterion():
    return minimium_money_question_page(1000, FORMS_SERVICE_PUBLIC_HOST)


@default_bp.route("/not-eligible")
def not_eligible():
    return render_template("not_eligible.html")


@default_bp.route("/continue_application", methods=["GET", "POST"])
def continue_application():
    """
    Page to return to an active application
    Provides a way of returning to an compelte/incomplete
        application to complete or make changes
    The user provides an application id and is redirected to
        the application summary page within the runner
    """
    form = FlaskForm()
    if request.method == "POST":
        application_id = request.form.get("application_id")
        application_data = get_application_data(application_id)
        if not application_data:
            return render_template(
                "continue_application.html",
                form=form,
                error=f"No data for this application: {application_id}",
            )
        form_id = application_data["fund_id"]
        formatted_application_payload = format_application_data(
            application_data, form_id
        )

        token = get_return_to_runner_token(
            form_id, formatted_application_payload
        )
        return redirect(f"{FORMS_SERVICE_PUBLIC_HOST}/session/{token}", 302)

    if request.method == "GET":
        return render_template("continue_application.html", form=form)


@default_bp.errorhandler(404)
def not_found(error):
    return render_template("404.html"), 404


@default_bp.errorhandler(500)
def internal_server_error(error):
    return render_template("500.html"), 500
