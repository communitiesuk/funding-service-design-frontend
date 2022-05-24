import requests
from app.config import FORM_GET_REHYDRATION_TOKEN_URL
from app.config import UPDATE_APPLICATION_SECTION_ENDPOINT
from slugify import slugify


def get_token_to_return_to_application(form_name: str, rehydrate_payload):
    res = requests.post(
        FORM_GET_REHYDRATION_TOKEN_URL.format(form_name=form_name),
        json=rehydrate_payload,
    )
    if res.status_code == 201:
        token_json = res.json()
        return token_json["token"]
    else:
        return None


def extract_subset_of_data_from_application(
    application_data: dict, data_subset_name: str
):
    """
    Returns a subset of application data.

            Parameters:
                    application_data (dict):
                     The application data for a single application,
                     returned from the application store
                    data_subset_name (str): The name of the application
                     data subset to be returned

            Returns:
                    application_data (dict):
                     A data subset of a single application
    """
    return application_data[data_subset_name]


def format_rehydrate_payload(micro_form_data, application_id, page_name):
    """
    Returns information in a JSON format that provides the
    POST body for the utilisation of the save and return
    functionality in the XGovFormBuilder

    Parameters:
        micro_form_data (dict):
        application data to reformat
        application_id (str):
        The id of an application in the application store
        page_name (str):
        The form page to redirect the user to.


    Returns:
        formatted_data (dict):
        formatted application data to rehydrate
            the xgov-form-runner
        formatted_data = {
            "options": {
                "callbackUrl": Str,
                "redirectPath": Str,
                "message": Str,
                "components": [],
                "customText": {
                    "paymentSkipped": false,
                    "nextSteps": false
                },
            },
            "questions": [],
            "metadata": {}
        }
    """

    formatted_data = {}
    redirect_path = slugify(f"{page_name}")
    callback_url = UPDATE_APPLICATION_SECTION_ENDPOINT

    formatted_data["options"] = {
        "callbackUrl": callback_url,
        "redirectPath": redirect_path,
        "customText": {"nextSteps": "Form Submitted"},
    }
    formatted_data["questions"] = extract_subset_of_data_from_application(
        micro_form_data, "questions"
    )
    formatted_data["metadata"] = extract_subset_of_data_from_application(
        micro_form_data, "metadata"
    )
    formatted_data["metadata"]["application_id"] = application_id
    return formatted_data
