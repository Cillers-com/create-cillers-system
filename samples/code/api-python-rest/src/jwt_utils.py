import os
import jwt as pyjwt
from jwt import PyJWKClient
from ssl import SSLContext, CERT_NONE, PROTOCOL_TLS_CLIENT
from typing import Optional
import logging

logger = logging.getLogger(__name__)

_SUPPORTED_JWT_ALGORITHMS = ['RS256', 'ES256', 'EdDSA']

AUTH_OIDC_JWKS_URL = os.getenv("JWT_OIDC_JWKS_URL")
AUTH_OIDC_AUDIENCE = os.getenv("JWT_OIDC_AUDIENCE")

def get_jwk_client():
    ssl_context = SSLContext(PROTOCOL_TLS_CLIENT)
    ssl_context.check_hostname = False
    ssl_context.verify_mode = CERT_NONE
    return PyJWKClient(AUTH_OIDC_JWKS_URL, ssl_context=ssl_context) if AUTH_OIDC_JWKS_URL else None

def verify_and_decode_jwt(token: str) -> Optional[dict]:
    try:
        client = get_jwk_client()
        if not client:
            logger.error("JWT client not initialized. Check JWT_OIDC_JWKS_URL environment variable.")
            return None
        signing_key = client.get_signing_key_from_jwt(token)
        result = pyjwt.decode(token,
                            signing_key.key,
                            algorithms=_SUPPORTED_JWT_ALGORITHMS,
                            audience=AUTH_OIDC_AUDIENCE,
                            options={'verify_exp': True})
        return result
    except pyjwt.PyJWTError:
        logger.exception("Failed to decode JWT")
        return None
