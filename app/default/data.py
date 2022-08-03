import json
import os

import requests
from config import Config
from flask import current_app

def get_data(endpoint: str):
    """
        Queries the api endpoint provided and returns a
        data response in json format.

    Args:
        endpoint (str): an API get data address

    Returns:
        data (json): data response in json format
    """

    current_app.logger.info(f"Fetching data from '{endpoint}'.")
    return (
        get_local_data(endpoint)
        if Config.USE_LOCAL_DATA
        else get_remote_data(endpoint)
    )


def get_remote_data(endpoint):
    response = requests.get(endpoint)
    if response.status_code == 200:
        data = response.json()
        return data
    else:
        return None


def get_local_data(endpoint: str):
    api_data_json = os.path.join(
        Config.FLASK_ROOT, "tests", "api_data", "endpoint_data.json"
    )

    fp = open(api_data_json)
    api_data = json.load(fp)
    fp.close()
    if endpoint in api_data:
        return api_data.get(endpoint)
    return None


def get_application_data(application_id):
    applications_endpoint = Config.GET_APPLICATION_ENDPOINT.format(
        application_id=application_id
    )
    applications_response = get_data(applications_endpoint)
    return applications_response
