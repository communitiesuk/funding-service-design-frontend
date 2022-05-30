import jwt as jwt
from app import config


def validate_token(token):
    return jwt.decode(token, config.RSA256_PUBLIC_KEY, algorithms=["RS256"])
