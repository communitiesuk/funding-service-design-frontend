"""Flask Production Environment Configuration."""
import base64
from os import environ

from config.envs.default import DefaultConfig
from fsd_utils import configclass


@configclass
class ProductionConfig(DefaultConfig):

    RSA256_PUBLIC_KEY = base64.b64decode(
        environ.get("RSA256_PUBLIC_KEY_BASE64")
    ).decode()
