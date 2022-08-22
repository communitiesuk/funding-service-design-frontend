import json
import os

import requests
from app.models.application import Application
from app.models.fund import Fund
from app.models.round import Round
from config import Config
from flask import abort
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
        current_app.logger.warn(
            "GET remote data call was unsuccessful with status code:"
            f" {response.status_code}."
        )
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


def get_application_data(application_id, as_dict=False):
    application_request_url = Config.GET_APPLICATION_ENDPOINT.format(
        application_id=application_id
    )
    application_response = get_data(application_request_url)
    if not (application_response):
        current_app.logger.error(
            "Application Data Store request failed, unable to recover:"
            f" {application_request_url}"
        )
        return abort(500)
    if as_dict:
        return Application.from_dict(application_response)
    else:
        return application_response


def get_fund_data(fund_id, as_dict=False):
    fund_request_url = Config.GET_FUND_DATA_ENDPOINT.format(fund_id=fund_id)
    fund_response = get_data(fund_request_url)
    if not fund_response:
        current_app.logger.error(
            f"Fund Store request failed, unable to recover: {fund_request_url}"
        )
        return abort(500)
    if as_dict:
        return Fund.from_dict(fund_response)
    else:
        return fund_response


def get_round_data(fund_id, round_id, as_dict=False):
    round_request_url = Config.GET_ROUND_DATA_FOR_FUND_ENDPOINT.format(
        fund_id=fund_id, round_id=round_id
    )
    round_response = get_data(round_request_url)
    if not round_response:
        current_app.logger.error(
            "Fund Store request failed, unable to recover:"
            f" {round_request_url}"
        )
        return abort(500)
    if as_dict:
        return Round.from_dict(round_response)
    else:
        return round_response
