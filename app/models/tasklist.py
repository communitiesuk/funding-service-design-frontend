from app.default.data import get_application_data
from flask import render_template
from flask_wtf import FlaskForm


def tasklist_page(application_id):
    """
    Returns a Flask function which constructs a tasklist for an application id.

    Args:
        application_id (str): the id of an application in the application store

    Returns:
        function: a function which renders the tasklist template.
    """
    application_response = get_application_data(application_id)
    application_meta_data = {
        "application_id": application_id,
        "round": application_response["round_id"],
        "fund": application_response["fund_id"],
        "number_of_sections": len(application_response["sections"]),
        "number_of_completed_sections": len(
            list(
                filter(
                    lambda section: section["status"] == "COMPLETED",
                    application_response["sections"],
                )
            )
        ),
        "number_of_incomplete_sections": len(
            list(
                filter(
                    lambda section: section["status"] == "NOT_STARTED",
                    application_response["sections"],
                )
            )
        ),
    }

    form = FlaskForm()
    return render_template(
        "tasklist.html",
        application_response=application_response,
        application_meta_data=application_meta_data,
        form=form,
    )
