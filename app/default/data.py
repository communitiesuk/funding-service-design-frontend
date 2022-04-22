import json
import os

import requests
from app.config import APPLICATION_STORE_API_HOST
from app.config import FLASK_ROOT

# Application Store Endpoints
APPLICATION_ENDPOINT = "/applications/{application_id}"


def get_data(endpoint: str):
    if endpoint[:8] == "https://":
        response = requests.get(endpoint)
        if response.status_code == 200:
            data = response.json()
        else:
            return None
    else:
        data = get_local_data(endpoint)
    return data


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


def extract_data_from_application(application_data, data_subset):
    data_subset = application_data[data_subset]
    return data_subset


def format_application_data(application_data, form_id):
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
    formatted_data["questions"] = extract_data_from_application(
        application_data, "questions"
    )
    formatted_data["metadata"] = extract_data_from_application(
        application_data, "metadata"
    )
    return formatted_data
