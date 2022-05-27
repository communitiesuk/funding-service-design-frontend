"""Flask configuration."""
from os import environ
from os import path

TEST_APPLICATION_STORE_API_HOST = "http://application_store"


# Application Config

SECRET_KEY = environ.get("SECRET_KEY") or "dev"
SESSION_COOKIE_NAME = environ.get("SESSION_COOKIE_NAME") or "session_cookie"
STATIC_FOLDER = "static"
TEMPLATES_FOLDER = "templates"
LOCAL_SERVICE_NAME = "local_flask"
FLASK_ROOT = path.dirname(path.dirname(path.realpath(__file__)))


# Forms Service Config

FORMS_SERVICE_NAME = environ.get("FORMS_SERVICE_NAME") or "xgov_forms_service"
FORMS_SERVICE_PUBLIC_HOST = (
    environ.get("FORMS_SERVICE_PUBLIC_HOST") or "http://localhost:3009"
)
FORMS_SERVICE_PREVIEW_HOST = (
    environ.get("FORMS_SERVICE_PREVIEW_HOST") or "http://localhost:3009"
)
FORMS_SERVICE_JSONS_PATH = (
    environ.get("FORMS_SERVICE_JSONS_PATH") or "form_jsons"
)
FORM_GET_REHYDRATION_TOKEN_URL = (
    FORMS_SERVICE_PUBLIC_HOST + "/session/{form_name}"
)
FORM_REHYDRATION_URL = (
    FORMS_SERVICE_PUBLIC_HOST + "/session/{rehydration_token}"
)


# Application Store Service Config

APPLICATION_STORE_API_HOST = (
    environ.get("APPLICATION_STORE_API_HOST")
    or TEST_APPLICATION_STORE_API_HOST
)
GET_APPLICATION_ENDPOINT = (
    APPLICATION_STORE_API_HOST + "/applications/{application_id}"
)
UPDATE_APPLICATION_SECTION_ENDPOINT = (
    APPLICATION_STORE_API_HOST + "/applications/sections"
)
SUBMIT_APPLICATION_ENDPOINT = (
    APPLICATION_STORE_API_HOST + "/applications/{application_id}/submit"
)

DEFAULT_FUND_ID = "funding-service-design"
DEFAULT_ROUND_ID = "summer"
