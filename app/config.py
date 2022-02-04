"""Flask configuration."""
from os import environ

"""
Application Config
"""
SECRET_KEY = environ.get("SECRET_KEY") or "dev"
SESSION_COOKIE_NAME = environ.get("SESSION_COOKIE_NAME") or "session_cookie"
STATIC_FOLDER = "static"
TEMPLATES_FOLDER = "templates"
LOCAL_SERVICE_NAME = "local_flask"

"""
Forms Service Config
"""
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
