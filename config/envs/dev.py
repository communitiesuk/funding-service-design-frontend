"""Flask Dev Pipeline Environment Configuration."""
import logging
from os import getenv

from config.envs.default import DefaultConfig
from fsd_utils import configclass


@configclass
class DevConfig(DefaultConfig):

    FSD_LOGGING_LEVEL = logging.INFO
    SESSION_COOKIE_DOMAIN = getenv("SESSION_COOKIE_DOMAIN")

    # Redis Feature Toggle Configuration
    REDIS_INSTANCE_NAME = "funding-service-magic-links-dev"
    REDIS_INSTANCE_URI = DefaultConfig.VCAP_SERVICES.get_service_credentials_value(
        "redis", REDIS_INSTANCE_NAME, "uri"
    )
    TOGGLES_URL = REDIS_INSTANCE_URI + "/0"
