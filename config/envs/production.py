"""Flask Production Environment Configuration."""
from config.envs.default import DefaultConfig
from fsd_utils import configclass


@configclass
class ProductionConfig(DefaultConfig):

    # Add any production specific config here

    pass
