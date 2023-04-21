"""Flask Test Environment Configuration."""
import base64
from os import environ

from config.envs.default import DefaultConfig
from fsd_utils import configclass


@configclass
class TestConfig(DefaultConfig):

    RSA256_PRIVATE_KEY = base64.b64decode(
        environ.get("RSA256_PRIVATE_KEY_BASE64")
    ).decode()
    RSA256_PUBLIC_KEY = base64.b64decode(
        environ.get("RSA256_PUBLIC_KEY_BASE64")
    ).decode()

    # Redis Feature Toggle Configuration
    REDIS_INSTANCE_NAME = "funding-service-magic-links-test"
    REDIS_INSTANCE_URI = (
        DefaultConfig.VCAP_SERVICES.get_service_credentials_value(
            "redis", REDIS_INSTANCE_NAME, "uri"
        )
    )
    TOGGLES_URL = REDIS_INSTANCE_URI + "/0"
