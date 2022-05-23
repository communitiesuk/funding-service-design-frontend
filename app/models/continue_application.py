import webbrowser

from app.default.data import get_application_data
from app.models.helpers import format_rehydrate_payload
from app.models.helpers import get_token_to_return_to_application


def continue_form_section(
    application_id: str, form_name: str, page_name: str, rehydration_url: str
):
    """
    Returns a Flask function to return to an active application form.
    This provides a way of returning to an applicants partially completed
        application.

    Args:
        application_id (str): The id of an application in the application store
        form_name (str): The name of the application sub form/section
        page_name (str): The form page to redirect the user to.

    Returns:
        A function: given a users application id they are redirected to
        the specified application form page within the form runner service
    """

    application_data = get_application_data(application_id)
    section_data = get_section_data(application_data, form_name)

    rehydrate_payload = format_rehydrate_payload(
        section_data, application_id, page_name
    )

    rehydration_token = get_token_to_return_to_application(
        form_name, rehydrate_payload
    )
    webbrowser.open_new_tab(
        rehydration_url.format(rehydration_token=rehydration_token)
    )


def get_section_data(application_data, form_name):
    forms_belonging_to_application = application_data["sections"]
    for form in forms_belonging_to_application:
        if form["section_name"] == form_name:
            return form
