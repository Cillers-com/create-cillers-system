import json
from datetime import timedelta
from typing import Annotated, Any, Dict
import logging

from couchbase.auth import PasswordAuthenticator
from couchbase.cluster import Cluster
from couchbase.exceptions import CouchbaseException
from couchbase.options import ClusterOptions, QueryOptions
from pydantic import BaseModel, StringConstraints, validate_arguments
from pydantic.networks import Url, UrlConstraints

logger = logging.getLogger(__name__)

#### Types ####

CouchbaseUrl = Annotated[
    Url,
    UrlConstraints(max_length=2083, allowed_schemes=["couchbase", "couchbases"]),
]

Username = Annotated[str, StringConstraints(pattern=r'^[a-zA-Z0-9._-]+$')]

class ConnectionConf(BaseModel):
    url: CouchbaseUrl
    username: Username
    password: str

class DocRef(BaseModel):
    bucket: str
    scope: str = '_default'
    collection: str = '_default'
    key: str

class DocSpec(BaseModel):
    key: str
    data: Any
    bucket: str
    scope: str = '_default'
    collection: str = '_default'

#### Utils ####

@validate_arguments
def get_authenticator(conf: ConnectionConf) -> PasswordAuthenticator:
    return PasswordAuthenticator(conf.username, conf.password)

@validate_arguments
def get_cluster(conf: ConnectionConf, timeout_s=5) -> Cluster:
    cluster = Cluster(str(conf.url), ClusterOptions(get_authenticator(conf)))
    cluster.wait_until_ready(timedelta(seconds=5))
    return cluster

#### Operations ####

@validate_arguments
def exec(conf: ConnectionConf, query: str, *args, **kwargs) -> Dict[str, Any]:
    log_str = "Running command {} ({}, {}) against {}".format(
        query, json.dumps(args), json.dumps(kwargs), conf.url
    )
    logger.debug(log_str)
    try:
        cluster = get_cluster(conf)

        result = cluster.query(query, QueryOptions(*args, **kwargs)).rows()
        result_list = list(result)

        logger.trace(f"{log_str} – got {result_list}")
        return result_list

    except CouchbaseException as e:
        logger.error(f"Couchbase error: {e}")
        raise

@validate_arguments
def insert(config: ConnectionConf, spec: DocSpec) -> Dict[str, Any]:
    return (get_cluster(config)
     .bucket(spec.bucket)
     .scope(spec.scope)
     .collection(spec.collection)
     .insert(spec.key, spec.data))

@validate_arguments
def remove(config: ConnectionConf, ref: DocRef) -> Dict[str, Any]:
    return (get_cluster(config)
     .bucket(ref.bucket)
     .scope(ref.scope)
     .collection(ref.collection)
     .remove(ref.key))

@validate_arguments
def get(config: ConnectionConf, ref: DocRef) -> Dict[str, Any]:
    return (get_cluster(config)
     .bucket(ref.bucket)
     .scope(ref.scope)
     .collection(ref.collection)
     .get(ref.key))
