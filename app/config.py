"""Flask configuration."""
from os import environ
from os import path

from dotenv import load_dotenv

basedir = path.abspath(path.dirname(__file__))
load_dotenv(path.join(basedir, ".env"))


class Config:
    """Base config."""

    SECRET_KEY = environ.get("SECRET_KEY") or "dev"
    SESSION_COOKIE_NAME = environ.get("SESSION_COOKIE_NAME") or "session_cookie"  # noqa
    STATIC_FOLDER = "static"
    TEMPLATES_FOLDER = "templates"
