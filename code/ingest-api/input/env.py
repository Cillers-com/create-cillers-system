import os
import logging

from . import http_server

logger = logging.getLogger(__name__)

## Auth ##

def get_auth_oidc_audience() -> str | None:
    return os.environ.get('AUTH_OIDC_AUDIENCE')

def get_auth_oidc_jwk_url() -> str | None:
    return os.environ.get('AUTH_OIDC_JWK_URL')

## HTTP ##

def get_http_port() -> int | None:
    if port :=  os.environ.get('HTTP_PORT'):
        try:
            return int(port)
        except ValueError:
            return None

def get_http_host() -> str:
    return os.environ.get('HTTP_HOST', '0.0.0.0')

def get_http_debug() -> bool:
    return os.environ.get('HTTP_DEBUG', 'false').lower() == 'true'

def get_http_autoreload() -> bool:
    return os.environ.get('HTTP_AUTORELOAD', 'false').lower() == 'true'

def get_http_graphql_ui() -> bool:
    return os.environ.get('HTTP_GRAPHQL_UI', 'false').lower() == 'true'

def get_http_conf() -> http_server.ServerConf:
    return http_server.ServerConf(
        port=int(get_http_port()),
        host=get_http_host(),
        debug=get_http_debug(),
        autoreload=get_http_autoreload()
    )

## Kafka ##

def get_kafka_broker() -> str | None:
    return os.environ.get('KAFKA_BROKER')

## Validation

def validate():
    ok = True
    if not get_auth_oidc_audience():
        logger.error('AUTH_OIDC_AUDIENCE is not set')
        ok = False
    if not get_auth_oidc_jwk_url():
        logger.error('AUTH_OIDC_JWK_URL is not set')
        ok = False
    if not get_http_port():
        logger.error('HTTP_PORT is not set')
        ok = False
    if not get_kafka_broker():
        logger.error('KAFKA_BROKER is not set')
        ok = False
    return ok
