from app.forms.eligibility_questions import form_page_from_criterion
from app.forms.eligibility_questions import must_be_atleast_criterion
from flask import Blueprint
from flask import render_template

bp = Blueprint("routes", __name__)


@bp.route("/")
def index():
    return render_template("index.html")


@bp.route("/funding_amount", methods=["GET", "POST"])
def funding_criterion():
    return form_page_from_criterion(must_be_atleast_criterion(10000))


@bp.errorhandler(404)
def not_found(error):
    return render_template("404.html"), 404


@bp.errorhandler(500)
def internal_server_error(error):
    return render_template("500.html"), 500
