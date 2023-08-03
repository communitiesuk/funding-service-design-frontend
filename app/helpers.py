from functools import lru_cache

import requests
from app.default.data import get_all_funds
from app.default.data import get_application_data
from app.default.data import get_default_round_for_fund
from app.default.data import get_fund_data
from app.default.data import get_fund_data_by_short_name
from app.default.data import get_round_data
from app.default.data import get_round_data_by_short_names
from app.default.data import get_ttl_hash
from app.models.fund import Fund
from config import Config
from flask import current_app
from flask import request


@lru_cache(maxsize=1)
def get_all_fund_short_codes(ttl_hash=get_ttl_hash(3000)):
    del ttl_hash  # only needed for lru_cache
    return [str.upper(fund.short_code) for fund in get_all_funds()]


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


def find_round_short_name_in_request():
    if round_short_name := request.view_args.get(
        "round_short_name"
    ) or request.args.get("round"):
        return round_short_name
    else:
        return None


def find_round_id_in_request():
    if (
        application_id := request.args.get("application_id")
        or request.view_args.get("application_id")
        or request.form.get("application_id")
    ):
        application = get_application_data(application_id, as_dict=True)
        return application.round_id
    else:
        return None


def find_fund_id_in_request():
    if fund_id := request.view_args.get("fund_id") or request.args.get(
        "fund_id"
    ):
        return fund_id
    elif (
        application_id := request.args.get("application_id")
        or request.view_args.get("application_id")
        or request.form.get("application_id")
    ):
        application = get_application_data(application_id, as_dict=True)
        return application.fund_id
    else:
        return None


def find_fund_short_name_in_request():
    if (
        fund_short_name := request.view_args.get("fund_short_name")
        or request.args.get("fund")
    ) and str.upper(fund_short_name) in get_all_fund_short_codes():
        return fund_short_name
    else:
        return None


def find_fund_in_request():
    return get_fund(
        find_fund_id_in_request(),
        find_fund_short_name_in_request(),
    )


def find_round_in_request(fund=None, fund_short_name=None):
    return get_round(
        fund=fund if fund else find_fund_in_request(),
        fund_short_name=fund_short_name,
        round_id=find_round_id_in_request(),
        round_short_name=find_round_short_name_in_request(),
    )


def find_fund_and_round_in_request():
    return get_fund_and_round(
        find_fund_id_in_request(),
        find_round_id_in_request(),
        find_fund_short_name_in_request(),
        find_round_short_name_in_request(),
    )


def get_fund_and_round(
    fund_id: str = None,
    round_id: str = None,
    fund_short_name: str = None,
    round_short_name: str = None,
):
    fund = get_fund(fund_id, fund_short_name)
    round = get_round(
        fund=fund, round_id=round_id, round_short_name=round_short_name
    )
    return fund, round


def get_fund(
    fund_id: str = None,
    fund_short_name: str = None,
):
    fund = (
        get_fund_data(fund_id, as_dict=False, ttl_hash=get_ttl_hash(3000))
        if fund_id
        else (
            get_fund_data_by_short_name(
                fund_short_name, as_dict=False, ttl_hash=get_ttl_hash(3000)
            )
            if fund_short_name
            else None
        )
    )
    return fund


def get_round(
    fund: Fund = None,
    fund_short_name: str = None,
    round_id: str = None,
    round_short_name: str = None,
):
    if fund_short_name:
        fund = get_fund_data_by_short_name(
            fund_short_name, ttl_hash=get_ttl_hash(300)
        )
    if not fund:
        return None
    round = (
        get_round_data(
            fund.id, round_id, as_dict=False, ttl_hash=get_ttl_hash(3000)
        )
        if round_id and fund
        else (
            get_round_data_by_short_names(
                fund.short_name,
                round_short_name,
                as_dict=False,
                ttl_hash=get_ttl_hash(3000),
            )
            if fund and round_short_name
            else None
        )
    )
    if not round:
        round = get_default_round_for_fund(fund.short_name)
    return round
