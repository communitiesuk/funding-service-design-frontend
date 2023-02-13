import requests
from config import Config
from flask import current_app


def get_token_to_return_to_application(form_name: str, rehydrate_payload):
    current_app.logger.info(
        "obtaining session rehydration token for application id:"
        f" {rehydrate_payload['metadata']['application_id']}."
    )
    res = requests.post(
        Config.FORM_GET_REHYDRATION_TOKEN_URL.format(form_name=form_name),
        json=rehydrate_payload,
    )
    if res.status_code == 201:
        token_json = res.json()
        return token_json["token"]
    else:
        raise Exception(
            "Unexpected response POSTing form token to"
            f" {Config.FORM_GET_REHYDRATION_TOKEN_URL.format(form_name=form_name)},"  # noqa: E501
            f" response code {res.status_code}"
        )


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


def format_rehydrate_payload(form_data, application_id, returnUrl, form_name):
    """
    Returns information in a JSON format that provides the
    POST body for the utilisation of the save and return
    functionality in the XGovFormBuilder
    PR instructions here:
    https://github.com/XGovFormBuilder/digital-form-builder/pull/760

    Parameters:
        form_data (dict):
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

    current_app.logger.info(
        "constructing session rehydration payload for application"
        f" id:{application_id}."
    )
    formatted_data = {}
    callback_url = Config.UPDATE_APPLICATION_FORM_ENDPOINT

    formatted_data["options"] = {
        "callbackUrl": callback_url,
        "customText": {"nextSteps": "Form Submitted"},
        "returnUrl": returnUrl,
    }
    formatted_data["questions"] = extract_subset_of_data_from_application(
        form_data, "questions"
    )
    formatted_data["metadata"] = {}
    formatted_data["metadata"]["application_id"] = application_id
    formatted_data["metadata"]["form_session_identifier"] = application_id
    formatted_data["metadata"]["form_name"] = form_name
    return formatted_data
