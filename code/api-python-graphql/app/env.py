import os
import logging
from pathlib import Path

from . import couchbase, http_server

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

## Couchbase ##

def get_couchbase_bucket() -> str:
    return os.environ.get('COUCHBASE_BUCKET', 'main')

def get_couchbase_url() -> str:
    return os.environ.get('COUCHBASE_URL', 'couchbase://couchbase')

def get_couchbase_username() -> str | None:
    return os.environ.get('COUCHBASE_USERNAME')

def get_couchbase_password() -> str | None:
    return os.environ.get('COUCHBASE_PASSWORD')

def get_couchbase_conf() -> couchbase.ConnectionConf:
    return couchbase.ConnectionConf(
        url=get_couchbase_url(),
        username=get_couchbase_username(),
        password=get_couchbase_password()
    )

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
    if not get_couchbase_username():
        logger.error('COUCHBASE_USERNAME is not set')
        ok = False
    if not get_couchbase_password():
        logger.error('COUCHBASE_PASSWORD is not set')
        ok = False
    return ok

def load_dotenv(filepath: Path):
    if os.path.exists(filepath):
        with open(filepath) as f:
            for line in f:
                line = line.strip()
                if not line or line.startswith('#'):
                    continue
                key, value = line.split('=', 1)
                if key and value:
                    os.environ[key] = value

env_file_path = Path('/root/conf/.env')
load_dotenv(env_file_path)
