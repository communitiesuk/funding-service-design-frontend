import json
import os

import requests
from app.config import FLASK_ROOT
from app.config import GET_APPLICATION_ENDPOINT


def get_data(endpoint: str):
    if endpoint.startswith("https://"):
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
    applications_endpoint = GET_APPLICATION_ENDPOINT.format(
        application_id=application_id
    )
    applications_response = get_data(applications_endpoint)
    return applications_response
