from functools import wraps

from app import config
from app.security.utils import validate_token
from flask import abort
from flask import request


def _check_access_token():
    login_cookie = request.cookies.get(config.FSD_USER_TOKEN_COOKIE_NAME)
    if login_cookie:
        valid_token = validate_token(login_cookie)
        return valid_token
    else:
        return abort(403)


def token_required(f):
    """Execute function if request contains valid access token."""

    @wraps(f)
    def decorated(*args, **kwargs):
        token_payload = _check_access_token()
        for name, val in token_payload.items():
            setattr(decorated, name, val)
        return f(*args, **kwargs)

    return decorated
