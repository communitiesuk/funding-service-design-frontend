from app.default.data import format_application_rehydrate_data
from app.default.data import get_application_data
from app.default.helpers import get_token_to_return_to_application
from flask import redirect
from flask import render_template
from flask import request
from flask_wtf import FlaskForm
from wtforms import StringField
from wtforms.validators import DataRequired


def continue_application_question_page(
    forms_service_host: str, application_id: str
):
    """
    Returns a Flask view function to return to an active application
    This provides a way of returning to an applicants partially completed
        application.

    Args:
        forms_service_host (str): The host name of the form runner service
        application_id (str): The id of an application in the application store

    Returns:
        A function: given a users application id they are redirected to
        the specified application summary page within the form runner service
    """

    class ContinueApplicationForm(FlaskForm):
        application_id = StringField(
            label="application_id",
            validators=[DataRequired()],
        )

    def continue_application_page(application_id):
        form = ContinueApplicationForm()
        if request.method == "POST":
            application_data = get_application_data(application_id)
            if not application_data:
                return render_template(
                    "continue_application.html",
                    form=form,
                    error=f"No data for this application: {application_id}",
                )
            form_id = application_data["fund_id"]
            formatted_application_payload = format_application_rehydrate_data(
                application_data
            )

            token = get_token_to_return_to_application(
                form_id, formatted_application_payload
            )
            return redirect(f"{forms_service_host}/session/{token}", 302)

        if request.method == "GET":
            return render_template("continue_application.html", form=form)

    return continue_application_page(application_id)
