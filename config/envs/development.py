"""Flask Local Development Environment Configuration."""
import logging

from config.envs.default import DefaultConfig
from fsd_utils import configclass


@configclass
class DevelopmentConfig(DefaultConfig):
    ALLOW_HTTP_API_CALLS = True
    FSD_LOGGING_LEVEL = logging.DEBUG
