"""Flask Production Environment Configuration."""
from os import environ

from config.envs.default import DefaultConfig
from fsd_utils import CommonConfig
from fsd_utils import configclass


@configclass
class ProductionConfig(DefaultConfig):

    # Redis Feature Toggle Configuration
    REDIS_INSTANCE_NAME = "funding-service-magic-links"

    if not hasattr(DefaultConfig, "VCAP_SERVICES"):
        REDIS_INSTANCE_URI = environ.get("REDIS_INSTANCE_URI", "redis://localhost:6379")
    else:
        REDIS_INSTANCE_URI = DefaultConfig.VCAP_SERVICES.get_service_credentials_value(
            "redis", REDIS_INSTANCE_NAME, "uri"
        )

    TOGGLES_URL = REDIS_INSTANCE_URI + "/0"
    FEATURE_CONFIG = CommonConfig.dev_feature_configuration
