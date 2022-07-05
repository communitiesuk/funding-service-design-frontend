"""Flask configuration."""
from os import environ
from pathlib import Path

from fsd_utils import configclass


@configclass
class DefaultConfig:
    """
    Application Config
    """

    FLASK_ENV = environ.get("FLASK_ENV", "development")
    SECRET_KEY = environ.get("SECRET_KEY", "dev")
    SESSION_COOKIE_NAME = environ.get("SESSION_COOKIE_NAME", "session_cookie")
    STATIC_FOLDER = "static"
    TEMPLATES_FOLDER = "templates"
    LOCAL_SERVICE_NAME = "local_flask"
    FLASK_ROOT = str(Path(__file__).parent.parent.parent)

    """
    APIs Config
    """
    TEST_APPLICATION_STORE_API_HOST = "http://application_store"

    APPLICATION_STORE_API_HOST = environ.get(
        "APPLICATION_STORE_API_HOST", TEST_APPLICATION_STORE_API_HOST
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

    FORMS_TEST_HOST = "http://localhost:3009"
    FORMS_SERVICE_NAME = environ.get(
        "FORMS_SERVICE_NAME", "xgov_forms_service"
    )
    FORMS_SERVICE_PUBLIC_HOST = environ.get(
        "FORMS_SERVICE_PUBLIC_HOST", FORMS_TEST_HOST
    )
    FORMS_SERVICE_PREVIEW_HOST = environ.get(
        "FORMS_SERVICE_PREVIEW_HOST", FORMS_TEST_HOST
    )
    FORMS_SERVICE_JSONS_PATH = "form_jsons"

    FORM_GET_REHYDRATION_TOKEN_URL = (
        FORMS_SERVICE_PUBLIC_HOST + "/session/{form_name}"
    )
    FORM_REHYDRATION_URL = (
        FORMS_SERVICE_PUBLIC_HOST + "/session/{rehydration_token}"
    )

    """Content Security Policy"""
    SECURE_CSP = {
        "default-src": "'self'",
        "script-src": [
            "'self'",
            "'sha256-+6WnXIl4mbFTCARd8N3COQmT3bJJmo32N8q8ZSQAIcU='",
            "'sha256-l1eTVSK8DTnK8+yloud7wZUqFrI0atVo6VlC6PJvYaQ='",
        ],
        "connect-src": "",  # APPLICATION_STORE_API_HOST_PUBLIC,
        "img-src": ["data:", "'self'"],
    }

    """Talisman Config"""

    # Security headers and other policies
    FSD_REFERRER_POLICY = "strict-origin-when-cross-origin"
    FSD_SESSION_COOKIE_SAMESITE = "Lax"
    FSD_PERMISSIONS_POLICY = {"interest-cohort": "()"}
    FSD_DOCUMENT_POLICY = {}
    FSD_FEATURE_POLICY = {
        "microphone": "'none'",
        "camera": "'none'",
        "geolocation": "'none'",
    }

    DENY = "DENY"
    SAMEORIGIN = "SAMEORIGIN"
    ALLOW_FROM = "ALLOW-FROM"
    ONE_YEAR_IN_SECS = 31556926

    FORCE_HTTPS = True

    TALISMAN_SETTINGS = {
        "feature_policy": FSD_FEATURE_POLICY,
        "permissions_policy": FSD_PERMISSIONS_POLICY,
        "document_policy": FSD_DOCUMENT_POLICY,
        "force_https": FORCE_HTTPS,
        "force_https_permanent": False,
        "force_file_save": False,
        "frame_options": "SAMEORIGIN",
        "frame_options_allow_from": None,
        "strict_transport_security": True,
        "strict_transport_security_preload": True,
        "strict_transport_security_max_age": ONE_YEAR_IN_SECS,
        "strict_transport_security_include_subdomains": True,
        "content_security_policy": SECURE_CSP,
        "content_security_policy_report_uri": None,
        "content_security_policy_report_only": False,
        "content_security_policy_nonce_in": None,
        "referrer_policy": FSD_REFERRER_POLICY,
        "session_cookie_secure": True,
        "session_cookie_http_only": True,
        "session_cookie_samesite": FSD_SESSION_COOKIE_SAMESITE,
        "x_content_type_options": True,
        "x_xss_protection": True,
    }
