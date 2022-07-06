import requests
from config import Config
from flask import current_app


def get_data(endpoint: str):
    if endpoint.startswith("https://") or Config.ALLOW_HTTP_API_CALLS:
        response = requests.get(endpoint)
        if response.status_code == 200:
            data = response.json()
        else:
            current_app.logger.warning(
                f"Function: {__name__} failed with status code"
                f" {response.status_code}."
            )
            return None
    else:
        current_app.logger.error(
            f"Function: {__name__} failed as the endpoint provided"
            f" ({endpoint}) is not https."
        )
        raise RuntimeError(f"The endpoint provided: {endpoint}, is not https.")
    return data


def get_application_data(application_id):
    applications_endpoint = Config.GET_APPLICATION_ENDPOINT.format(
        application_id=application_id
    )
    return get_data(applications_endpoint)
