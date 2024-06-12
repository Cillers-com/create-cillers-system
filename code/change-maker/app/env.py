import os
import logging

from . import couchbase

logger = logging.getLogger(__name__)

## Couchbase ##

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
    if not get_couchbase_username():
        logger.error('COUCHBASE_USERNAME is not set')
        ok = False
    if not get_couchbase_password():
        logger.error('COUCHBASE_PASSWORD is not set')
        ok = False
    return ok
