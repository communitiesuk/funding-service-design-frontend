from flask import Blueprint
from flask import render_template
from formuli.formuli import Formuli

bp = Blueprint(
    "formuli", __name__, url_prefix="/formuli", template_folder="templates"
)  # noqa


@bp.route("/")
def example_form():

    formuli = Formuli()

    return render_template("formuli/formuli.html", formuli=formuli)
