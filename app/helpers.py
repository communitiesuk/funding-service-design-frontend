import requests
from app.default.data import get_application_data
from app.default.data import get_default_round_for_fund
from app.default.data import get_fund_data
from app.default.data import get_fund_data_by_short_name
from app.default.data import get_round_data
from app.default.data import get_round_data_by_short_names
from app.models.fund import Fund
from app.models.fund import FUND_SHORT_CODES
from app.models.round import Round
from config import Config
from flask import current_app
from flask import request
from flask import session


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


def find_round_in_request(fund):
    round = None
    if round_short_name := request.view_args.get(
        "round_short_name"
    ) or request.args.get("round"):
        round = get_round_data_by_short_names(
            fund.short_name, round_short_name, False
        )
    elif (
        application_id := request.args.get("application_id")
        or request.view_args.get("application_id")
        or request.form.get("application_id")
    ):
        application = get_application_data(application_id, as_dict=True)
        round = get_round_data(
            fund_id=application.fund_id,
            round_id=application.round_id,
            language=application.language,
        )

    if not round:
        round = get_default_round_for_fund(fund.short_name)
        current_app.logger.warn(
            "Couldn't find round in request. Using"
            f" {round.short_name} as default for fund {fund.short_name}"
        )
    return round


def find_fund_in_request():
    if (
        fund_short_name := request.view_args.get("fund_short_name")
        or request.args.get("fund")
    ) and str.upper(fund_short_name) in [
        member.value for member in FUND_SHORT_CODES
    ]:
        fund = get_fund_data_by_short_name(fund_short_name, as_dict=False)
    elif fund_id := request.view_args.get("fund_id") or request.args.get(
        "fund_id"
    ):
        fund = get_fund_data(fund_id, as_dict=True)
    elif (
        application_id := request.args.get("application_id")
        or request.view_args.get("application_id")
        or request.form.get("application_id")
    ):
        application = get_application_data(application_id, as_dict=True)
        fund = get_fund_data(
            fund_id=application.fund_id,
            language=application.language,
            as_dict=True,
        )
    else:
        current_app.logger.warn("Couldn't find any fund in the request")
        return None
    return fund


CACHED_FUND_ROUNDS_PROPERTY = "cached_fund_rounds"
FUNDS_BY_ID_PROPERTY = "funds_by_id"
FUNDS_BY_SHORT_NAME_PROPERTY = "funds_by_short_name"
ROUNDS_BY_ID_PROPERTY = "rounds_by_id"
ROUNDS_BY_SHORT_NAME_PROPERTY = "rounds_by_short_name"


def get_fund_and_round(
    fund_id: str = None,
    round_id: str = None,
    fund_short_name: str = None,
    round_short_name: str = None,
):
    fund = None
    round = None
    if cached_fund_rounds := session.get(CACHED_FUND_ROUNDS_PROPERTY):
        fund = (
            Fund.from_dict(
                cached_fund_rounds.get(FUNDS_BY_ID_PROPERTY).get(fund_id)
            )
            if fund_id
            else (
                Fund.from_dict(
                    cached_fund_rounds.get(FUNDS_BY_SHORT_NAME_PROPERTY).get(
                        str.upper(fund_short_name)
                    )
                )
                if fund_short_name
                else None
            )
        )

        round = (
            Round.from_dict(
                cached_fund_rounds.get(ROUNDS_BY_ID_PROPERTY).get(round_id)
            )
            if round_id
            else (
                Round.from_dict(
                    cached_fund_rounds.get(ROUNDS_BY_SHORT_NAME_PROPERTY).get(
                        str.upper(round_short_name)
                    )
                )
                if round_short_name
                else None
            )
        )

        if fund and round:
            return fund, round

    if not cached_fund_rounds:
        cached_fund_rounds = {}
    fund = (
        get_fund_data(fund_id, as_dict=False)
        if fund_id
        else (
            get_fund_data_by_short_name(fund_short_name, as_dict=False)
            if fund_short_name
            else None
        )
    )
    round = (
        get_round_data(fund_id, round_id, as_dict=False)
        if round_id and fund_id
        else (
            get_round_data_by_short_names(
                fund_short_name, round_short_name, as_dict=False
            )
            if fund_short_name and round_short_name
            else None
        )
    )
    cached_fund_rounds[FUNDS_BY_ID_PROPERTY] = {fund.id: fund}
    cached_fund_rounds[FUNDS_BY_SHORT_NAME_PROPERTY] = {fund.short_name: fund}
    cached_fund_rounds[ROUNDS_BY_ID_PROPERTY] = {round.id: round}
    cached_fund_rounds[ROUNDS_BY_SHORT_NAME_PROPERTY] = {
        round.short_name: round
    }
    session[CACHED_FUND_ROUNDS_PROPERTY] = cached_fund_rounds
    return fund, round
