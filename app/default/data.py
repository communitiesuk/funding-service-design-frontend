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
            f"Function: {__name__} failed as the endpoint provided:"
            f" {endpoint}, is not using https."
        )
        raise RuntimeError(
            f"The endpoint provided: {endpoint}, is not using https."
        )
    return data
