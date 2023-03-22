import json
import os
from urllib.parse import urlencode

import requests
from app.models.account import Account
from app.models.application import Application
from app.models.fund import Fund
from app.models.round import Round
from config import Config
from flask import abort
from flask import current_app
from fsd_utils.locale_selector.get_lang import get_lang


def get_data(endpoint: str, params: dict = None):
    """
        Queries the api endpoint provided and returns a
        data response in json format.

    Args:
        endpoint (str): an API get data address

    Returns:
        data (json): data response in json format
    """

    query_string = ""
    if params:
        params = {k: v for k, v in params.items() if v is not None}
        query_string = urlencode(params)
        endpoint = endpoint + "?" + query_string

    if Config.USE_LOCAL_DATA:
        current_app.logger.info(f"Fetching local data from '{endpoint}'.")
        data = get_local_data(endpoint)
    else:
        current_app.logger.info(f"Fetching data from '{endpoint}'.")
        data = get_remote_data(endpoint)
    if data is None:
        current_app.logger.error(
            f"Data request failed, unable to recover: {endpoint}"
        )
        return abort(500)
    return data


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
    with open(api_data_json) as json_file:
        api_data = json.load(json_file)
    if endpoint in api_data:
        mocked_response = requests.models.Response()
        mocked_response.status_code = 200
        content_str = json.dumps(api_data[endpoint])
        mocked_response._content = bytes(content_str, "utf-8")
        return json.loads(mocked_response.text)
    return None


def get_application_data(application_id, as_dict=False):
    application_request_url = Config.GET_APPLICATION_ENDPOINT.format(
        application_id=application_id
    )
    application_response = get_data(application_request_url)
    if as_dict:
        return Application.from_dict(application_response)
    else:
        return application_response


def get_applications_for_account(account_id, as_dict=False):
    application_request_url = (
        Config.GET_APPLICATIONS_FOR_ACCOUNT_ENDPOINT.format(
            account_id=account_id
        )
    )
    application_response = get_data(application_request_url)
    if as_dict:
        return Application.from_dict(application_response)
    else:
        return application_response


def get_fund_data(fund_id, language=None, as_dict=False):
    language = {"language": language or get_lang()}
    fund_request_url = Config.GET_FUND_DATA_ENDPOINT.format(fund_id=fund_id)
    fund_response = get_data(fund_request_url, language)
    if as_dict:
        return Fund.from_dict(fund_response)
    else:
        return fund_response


def get_round_data(fund_id, round_id, language=None, as_dict=False):
    language = {"language": language or get_lang()}
    round_request_url = Config.GET_ROUND_DATA_FOR_FUND_ENDPOINT.format(
        fund_id=fund_id, round_id=round_id
    )
    round_response = get_data(round_request_url, language)
    if as_dict:
        return Round.from_dict(round_response)
    else:
        return round_response


def get_round_data_by_short_names(fund_short_name, round_short_name):
    request_url = Config.GET_ALL_ROUNDS_FOR_FUND_ENDPOINT.format(
        fund_id=fund_short_name
    )
    response = get_data(
        request_url, {"language": get_lang(), "use_short_name": "true"}
    )
    return next(
        (
            round
            for round in response
            if str.casefold(round["short_name"])
            == str.casefold(round_short_name)
        ),
        None,
    )


def get_round_data_fail_gracefully(fund_id, round_id):
    try:
        language = {"language": get_lang()}
        round_request_url = Config.GET_ROUND_DATA_FOR_FUND_ENDPOINT.format(
            fund_id=fund_id, round_id=round_id
        )
        round_response = get_data(round_request_url, language)
        return Round.from_dict(round_response)
    except:  # noqa
        current_app.logger.error(
            f"Call to Fund Store failed GET { round_request_url }"
        )
        # return valid Round object with no values so we know we've
        # failed and can handle in templates appropriately
        return Round("", [], "", "", "", "", "", "", {}, {})


def get_account(email: str = None, account_id: str = None) -> Account | None:
    """
    Get an account from the account store using either
    an email address or account_id.

    Args:
        email (str, optional): The account email address
        Defaults to None.
        account_id (str, optional): The account id. Defaults to None.

    Raises:
        TypeError: If both an email address or account id is given,
        a TypeError is raised.

    Returns:
        Account object or None
    """
    if email is account_id is None:
        raise TypeError("Requires an email address or account_id")

    url = Config.ACCOUNT_STORE_API_HOST + Config.ACCOUNTS_ENDPOINT
    params = {"email_address": email, "account_id": account_id}
    response = get_data(url, params)

    if response and "account_id" in response:
        return Account.from_json(response)


def get_all_funds():
    language = {"language": get_lang()}
    fund_response = get_data(Config.GET_ALL_FUNDS_ENDPOINT, language)
    return fund_response


def get_all_rounds_for_fund(fund_id):
    language = {"language": get_lang()}
    rounds_response = get_data(
        Config.GET_ALL_ROUNDS_FOR_FUND_ENDPOINT.format(fund_id=fund_id),
        language,
    )
    return rounds_response
