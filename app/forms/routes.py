from flask import Blueprint
from flask import render_template

from .formzy import create_formzy_with_json

forms_bp = Blueprint(
    "forms_bp", __name__, url_prefix="/forms", template_folder="templates"
)


@forms_bp.route("/", methods=["GET"])
def landing_page():

    formzy = create_formzy_with_json()

    return render_template("landing.html", formzy=formzy)


@forms_bp.route("/<form_name>/", methods=["GET", "POST"])
def form_steps(form_name: str):

    formzy = create_formzy_with_json()

    return render_template("steps.html", formzy=formzy)
