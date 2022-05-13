import json
import os

import requests
from app.config import APPLICATION_STORE_API_HOST
from app.config import FLASK_ROOT

# Application Store Endpoints
APPLICATION_ENDPOINT = "/applications/{application_id}"


def get_data(endpoint: str):
    if endpoint[:8] == "https://":
        data = get_remote_data(endpoint)
    else:
        data = get_local_data(endpoint)
    return data


def get_remote_data(endpoint):
    response = requests.get(endpoint)
    if response.status_code == 200:
        data = response.json()
        return data
    else:
        return None


def get_local_data(endpoint: str):
    api_data_json = os.path.join(
        FLASK_ROOT, "tests", "api_data", "endpoint_data.json"
    )
    fp = open(api_data_json)
    api_data = json.load(fp)
    fp.close()
    if endpoint in api_data:
        return api_data.get(endpoint)
    return None


def get_application_data(application_id):
    applications_endpoint = (
        APPLICATION_STORE_API_HOST
        + APPLICATION_ENDPOINT.format(application_id=application_id)
    )
    applications_response = get_data(applications_endpoint)
    return applications_response


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


def format_application_rehydrate_data(application_data):
    """
    Returns information in a JSON format that provides the
     POST body for the utilisation of the save and return
     functionality of the XGovFormBuilder

            Parameters:
                    application_data (dict): application data to reformat

            Returns:
                    formatted_data (dict): formatted application data
    """

    formatted_data = {}
    redirect_path = "/summary"

    """
    formatted_data = {
        "options": {
            "callbackUrl": Str,
            "redirectPath": Str,
            "message": Str,
            "components": [], // extra components to show on page?
            "customText": {
                "paymentSkipped": false,
                "nextSteps": false
            },
        },
        "questions": [],
        "metadata": {}
    }
    """

    formatted_data["options"] = {"redirectPath": redirect_path}
    formatted_data["questions"] = extract_subset_of_data_from_application(
        application_data, "questions"
    )
    formatted_data["metadata"] = extract_subset_of_data_from_application(
        application_data, "metadata"
    )
    return formatted_data
