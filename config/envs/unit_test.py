"""Flask Local Development Environment Configuration."""
from config.envs.default import DefaultConfig
from fsd_utils import CommonConfig
from fsd_utils import configclass


@configclass
class UnitTestConfig(DefaultConfig):
    DefaultConfig.TALISMAN_SETTINGS["force_https"] = False
    USE_LOCAL_DATA = "True"
    SESSION_COOKIE_SECURE = False

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

    WTF_CSRF_ENABLED = False

    FORMS_CONFIG_FOR_FUND_ROUND = {
        "funding-service-design:summer": CommonConfig.COF_R2_ORDERED_FORMS_CONFIG,  # noqa
    }

    # Redis Configuration for Feature Flags
    REDIS_MLINKS_URL = "redis://localhost:6379/0"
