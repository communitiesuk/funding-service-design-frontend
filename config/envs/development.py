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
