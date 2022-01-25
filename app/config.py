"""Flask configuration."""
from os import environ

"""
Application Config
"""
SECRET_KEY = environ.get("SECRET_KEY") or "dev"
SESSION_COOKIE_NAME = environ.get("SESSION_COOKIE_NAME") or "session_cookie"
STATIC_FOLDER = "static"
TEMPLATES_FOLDER = "templates"

"""
Forms Service Config
"""
FORMS_SERVICE_NAME = environ.get("FORMS_SERVICE_NAME") or "xgov_forms_service"
FORMS_SERVICE_HOST = (
    environ.get("FORMS_SERVICE_HOST") or "http://localhost:3009"
)
FORMS_SERVICE_TEST_PUBLIC_FORM = (
    environ.get("FORMS_SERVICE_TEST_PUBLIC_FORM") or 0
)
FORMS_SERVICE_TEST_FORM = (
    environ.get("FORMS_SERVICE_TEST_FORM") or "simple-three-step-form"
)
FORMS_SERVICE_JSONS_PATH = (
    environ.get("FORMS_SERVICE_JSONS_PATH") or "form_jsons"
)
