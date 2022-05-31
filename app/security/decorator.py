from functools import wraps

from app import config
from app.security.utils import validate_token
from flask import redirect
from flask import request


def _check_access_token():
    login_cookie = request.cookies.get(config.FSD_USER_TOKEN_COOKIE_NAME)
    if login_cookie:
        valid_token = validate_token(login_cookie)
        return valid_token
    else:
        return redirect(
            f"{config.AUTHENTICATOR_HOST}/magic-links/"
            f"new?return_url={request.url}"
        )


def login_required(f):
    """Execute function if request contains valid JWT
    and pass account_id to route."""

    @wraps(f)
    def decorated(*args, **kwargs):
        token_payload = _check_access_token()
        kwargs["account_id"] = token_payload.get("accountId")
        return f(*args, **kwargs)

    return decorated
