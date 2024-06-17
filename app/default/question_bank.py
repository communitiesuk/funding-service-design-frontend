import json

from flask import Blueprint
from flask import render_template
from flask import request
from flask import Response
from scripts.question_reuse.config.pages_to_reuse import PAGES_TO_REUSE
from scripts.question_reuse.generate_form import build_form_json

qb_bp = Blueprint("question_bank", __name__, template_folder="templates")


@qb_bp.route("/question_bank")
def question_bank():
    return render_template(
        "question_bank.html", available_pages=PAGES_TO_REUSE
    )


@qb_bp.route("/generate_form", methods=["POST"])
def generate_form():
    pages = request.form.getlist("selected_pages")
    title = request.form.get("form_title")
    input_data = {"title": title, "pages": pages}
    form_json = build_form_json(input_data)
    form_json["name"] = "QB: " + form_json["name"]

    return Response(
        response=json.dumps(form_json),
        mimetype="application/json",
        headers={"Content-Disposition": "attachment;filename=form.json"},
    )
