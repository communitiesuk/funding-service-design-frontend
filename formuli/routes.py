from flask import Blueprint
from flask import render_template
from formuli.formuli import create_form_with_json

bp = Blueprint(
    "formuli", __name__, url_prefix="/formuli", template_folder="templates"
)  # noqa


@bp.route("/", methods=["GET", "POST"])
def example_form():

    formuli = create_form_with_json()

    return render_template("formuli/formuli.html", formuli=formuli)
