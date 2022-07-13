"""Flask Local Development Environment Configuration."""
import logging
from os import getenv

from config.envs.default import DefaultConfig
from distutils.util import strtobool
from fsd_utils import configclass


@configclass
class DevelopmentConfig(DefaultConfig):

    FSD_LOGGING_LEVEL = logging.DEBUG
    USE_LOCAL_DATA = strtobool(getenv("USE_LOCAL_DATA", "True"))

    COOKIE_DOMAIN = getenv("COOKIE_DOMAIN", ".localhost.localhost")
    SESSION_COOKIE_DOMAIN = getenv("SESSION_COOKIE_DOMAIN")

    # RSA 256 KEYS
    _test_private_key_path = (
        DefaultConfig.FLASK_ROOT + "/tests/keys/rsa256/private.pem"
    )
    with open(_test_private_key_path, mode="rb") as private_key_file:
        RSA256_PRIVATE_KEY = private_key_file.read()
    _test_public_key_path = (
        DefaultConfig.FLASK_ROOT + "/tests/keys/rsa256/public.pem"
    )
    with open(_test_public_key_path, mode="rb") as public_key_file:
        RSA256_PUBLIC_KEY = public_key_file.read()
