import requests
from flask import Blueprint
from flask import current_app
from flask import redirect
from flask import render_template
from flask import url_for
from flask import request

from app.config import FORMS_SERVICE_PUBLIC_HOST
from app.forms.eligibility_questions import minimium_money_question_page
from app.models.application_summary import ApplicationSummary

default_bp = Blueprint("routes", __name__, template_folder="templates")


@default_bp.route("/")
def index():
    return render_template(
        "index.html", service_url=url_for("routes.max_funding_criterion")
    )


@default_bp.route("/account/<account_id>")
def dashboard(account_id):
    response = requests.get(
        f'{current_app.config.get("APPLICATION_STORE_HOST")}/applications?account_id={account_id}'
    ).json()
    applications: list[ApplicationSummary] = [ApplicationSummary.from_dict(application) for application in response]
    return render_template("dashboard.html", account_id=account_id, applications=applications)


@default_bp.route("/account/<account_id>/new", methods=['POST'])
def new(account_id):
    new_application = requests.post(url=f'{current_app.config.get("APPLICATION_STORE_HOST")}/applications',
                                    json={'account_id': account_id,
                                          'round_id': request.form['round_id'],
                                          'fund_id': request.form['fund_id']
                                          }
                                    )
    return redirect(f'/tasklist/{new_application.json().get("id")}')


@default_bp.route("/funding_amount_eligibility", methods=["GET", "POST"])
def max_funding_criterion():
    return minimium_money_question_page(1000, FORMS_SERVICE_PUBLIC_HOST)


@default_bp.route("/not-eligible")
def not_eligible():
    return render_template("not_eligible.html")


@default_bp.errorhandler(404)
def not_found(error):
    return render_template("404.html"), 404


@default_bp.errorhandler(500)
def internal_server_error(error):
    return render_template("500.html"), 500
