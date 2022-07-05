"""Flask Local Development Environment Configuration."""
from config.envs.default import DefaultConfig
from fsd_utils import configclass


@configclass
class UnitTestConfig(DefaultConfig):
    DefaultConfig.TALISMAN_SETTINGS["force_https"] = False
