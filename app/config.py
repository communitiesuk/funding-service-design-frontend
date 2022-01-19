"""Flask configuration."""
import os

TESTING = True
DEBUG = True
SECRET_KEY = os.environ.get("SECRET_KEY")
