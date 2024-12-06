"""Flask Production Environment Configuration."""

from fsd_utils import configclass

from config.envs.default import DefaultConfig


@configclass
class ProductionConfig(DefaultConfig):
    pass
