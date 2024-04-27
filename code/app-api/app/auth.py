import jwt
from jwt import PyJWKClient
import logging
from ssl import SSLContext, CERT_NONE, PROTOCOL_TLS_CLIENT
from typing import Optional

from . import env

logger = logging.getLogger(__name__)

#### Constants ####

_SUPPORTED_JWT_ALGORITHMS = ['RS256', 'ES256', 'EdDSA']

#### Decoding ####

def get_jwk_client():
    "Builds a JWK client."
    # TODO: make Curity use a trusted SSL certificate so we don't have to do this
    ssl_context = SSLContext(PROTOCOL_TLS_CLIENT)
    ssl_context.check_hostname = False
    ssl_context.verify_mode = CERT_NONE
    return PyJWKClient(env.get_auth_oidc_jwk_url(), ssl_context=ssl_context)

def verify_and_decode_jwt(token: str) -> Optional[dict]:
    "Decodes a JWT using the configures JWKS URL and audience."
    try:
        client = get_jwk_client()
        signing_key = client.get_signing_key_from_jwt(token)
        result = jwt.decode(token,
                            signing_key.key,
                            algorithms=_SUPPORTED_JWT_ALGORITHMS,
                            audience=env.get_auth_oidc_audience(),
                            options={'verify_exp': True})
        return result
    except jwt.PyJWTError:
        logger.exception("Failed to decode JWT")
        pass
