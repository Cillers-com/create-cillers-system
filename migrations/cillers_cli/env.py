import os
from typing import Any, Callable

from pydantic import (
    BaseModel,
    ValidationError,
    create_model,
    validate_arguments,
)

from . import log, couchbase, kafka, kafka_connect, types

logger = log.get_logger(__name__)

class EnvVarSpec(BaseModel):
    id: str
    type: Any = (str, ...)
    parse: Callable[[str], Any] = None
    is_optional: bool = False
    is_secret: bool = False

COUCHBASE_URL = EnvVarSpec(id='COUCHBASE_URL',
                           type=(couchbase.CouchbaseUrl, ...))
COUCHBASE_USERNAME = EnvVarSpec(id='COUCHBASE_USERNAME',
                                type=(couchbase.Username, ...))
COUCHBASE_PASSWORD = EnvVarSpec(id='COUCHBASE_PASSWORD', is_secret=True)
KAFKA_BOOTSTRAP_SERVERS = EnvVarSpec(id='KAFKA_BOOTSTRAP_SERVERS',
                                     type=(kafka.BootstrapServers, ...))
KAFKA_CONNECT_BASE_URL = EnvVarSpec(id='KAFKA_CONNECT_BASE_URL',
                                    type=(kafka_connect.BaseUrl, ...))

ENV_VARS: list[EnvVarSpec] = [COUCHBASE_URL,
                              COUCHBASE_USERNAME,
                              COUCHBASE_PASSWORD,
                              KAFKA_BOOTSTRAP_SERVERS,
                              KAFKA_CONNECT_BASE_URL]

class UnsetException(Exception):
    pass

class ValidationException(Exception):
    def __init__(self, message, value):
        super().__init__(message)
        self.value = value

class ParseException(Exception):
    def __init__(self, message, value):
        super().__init__(message)
        self.value = value

def check(label, value, t):
    M = create_model(label, x=t)
    result = M(**{'x': value})
    return result

@validate_arguments
def parse(var: EnvVarSpec):
    if value := os.environ.get(var.id):
        if parse := var.parse:
            try:
                value = parse(value)
            except Exception as e:
                raise ParseException(f"Failed to parse {var.id}: {str(e)}",
                                     value=value)
        try:
            check(var.id, value, var.type)
        except ValidationError as e:
            raise ValidationException(f"Failed to validate {var.id}: {str(e)}",
                                      value=value)
        return value
    else:
        if var.is_optional:
            return None
        else:
            raise UnsetException(f"{var.id} is unset")

def validate() -> bool:
    ok = True
    for var in ENV_VARS:
        try:
            value = parse(var)
            logger.info(
                "Env var %s is set to %s",
                log.blue(var.id),
                log.cyan('<REDACTED>') if var.is_secret else log.cyan(value),
            )
        except UnsetException:
            logger.error(f"Env var {log.blue(var.id)} is {log.red('unset')}")
            ok = False
        except ParseException as e:
            logger.error(
                "Env var %s (set to %s) failed to parse:\n%s",
                log.blue(var.id),
                log.cyan('<REDACTED>') if var.is_secret else log.cyan(e.value),
                log.red(str(e))
            )
            ok = False
        except ValidationException as e:
            logger.error(
                "Env var %s (set to %s) is invalid:\n%s",
                log.blue(var.id),
                log.cyan('<REDACTED>') if var.is_secret else log.cyan(e.value),
                log.red(str(e))
            )
            ok = False
    return ok

def get_couchbase_config() -> couchbase.ConnectionConf:
    return couchbase.ConnectionConf(
        url=parse(COUCHBASE_URL),
        username=parse(COUCHBASE_USERNAME),
        password=parse(COUCHBASE_PASSWORD),
    )

def get_kafka_config() -> kafka.ConnectionConf:
    return kafka.ConnectionConf(
        bootstrap_servers=parse(KAFKA_BOOTSTRAP_SERVERS)
    )

def get_kafka_connect_config() -> kafka_connect.ConnectionConf:
    return kafka_connect.ConnectionConf(
        base_url=parse(KAFKA_CONNECT_BASE_URL)
    )

def get_configs() -> types.ConnectionConfs:
    return types.ConnectionConfs(kafka=get_kafka_config(),
                                 kafka_connect=get_kafka_connect_config(),
                                 couchbase=get_couchbase_config())
