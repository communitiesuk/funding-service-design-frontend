"""Flask Production Environment Configuration."""
from config.envs.default import DefaultConfig
from fsd_utils import CommonConfig
from fsd_utils import configclass


@configclass
class ProductionConfig(DefaultConfig):

    # Redis Feature Toggle Configuration
    REDIS_INSTANCE_NAME = "funding-service-magic-links"
    REDIS_INSTANCE_URI = (
        DefaultConfig.VCAP_SERVICES.get_service_credentials_value(
            "redis", REDIS_INSTANCE_NAME, "uri"
        )
    )
    FEATURE_CONFIG = CommonConfig.prod_feature_configuration
