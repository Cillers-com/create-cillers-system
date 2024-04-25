import json
from datetime import datetime, timedelta
from enum import Enum
from typing import Annotated, Any, Dict, Optional, Union

import couchbase.management.collections as collections
from couchbase.auth import PasswordAuthenticator
from couchbase.cluster import Cluster
from couchbase.exceptions import (
    BucketAlreadyExistsException,
    BucketDoesNotExistException,
    BucketNotFoundException,
    CollectionAlreadyExistsException,
    CouchbaseException,
    QueryIndexAlreadyExistsException,
)
from couchbase.management.buckets import (
    BucketSettings,
    BucketType,
    CompressionMode,
    ConflictResolutionType,
    CreateBucketSettings,
    EvictionPolicyType,
    StorageBackend,
)
from couchbase.options import ClusterOptions, QueryOptions
from pydantic import BaseModel, StringConstraints, validate_arguments
from pydantic.networks import Url, UrlConstraints

from . import log

logger = log.get_logger(__name__)

#### Constants ####

MIGRATIONS_BUCKET='cillers'
MIGRATIONS_COLLECTION='migrations'

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

class BucketSpec(BaseModel):
    name: str
    ram_quota_mb: int
    bucket_type: BucketType = BucketType.COUCHBASE
    flush_enabled: bool = None
    num_replicas: int = None
    replica_index: bool = None
    eviction_policy: EvictionPolicyType = None
    max_expiry: Union[timedelta, float, int] = None
    compression_mode: CompressionMode = None
    conflict_resolution_type: ConflictResolutionType = None
    bucket_password: Optional[str] = None
    storage_backend: StorageBackend = None

    class Config:
        use_enum_values = True

class CollectionSpec(BaseModel):
    name: str
    bucket: str
    scope: str = '_default'
    max_expiry: timedelta = None

class DocSpec(BaseModel):
    key: str
    data: Any
    bucket: str
    scope: str = '_default'
    collection: str = '_default'

class MigrationRecord(BaseModel):
    ts: str
    id: str

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
def ensure_bucket_exists(conf: ConnectionConf, spec: BucketSpec):
    cluster = get_cluster(conf)
    manager = cluster.buckets()

    try:
        bucket = manager.get_bucket(spec.name)
        diff = {}
        for k, v in spec.dict(exclude_unset=True).items():
            old = bucket.get(k)
            if isinstance(old, Enum):
                old = old.value
            if old != v:
                diff[k] = {'old': old, 'new': v}

        if diff:
            logger.info('Applying diff to bucket %s: %s',
                        log.blue(spec.name), diff)
            manager.update_bucket(BucketSettings(**spec.dict(exclude_unset=True)))
            logger.info(f"Bucket {log.blue(spec.name)} modified.")
    except (BucketDoesNotExistException, BucketNotFoundException):
        try:
            manager.create_bucket(CreateBucketSettings(**spec.dict(exclude_unset=True)))
            logger.info(f"Bucket {log.blue(spec.name)} created.")
            # TODO: wait for the bucket to be ready
        except BucketAlreadyExistsException:
            pass


@validate_arguments
def ensure_collection_exists(conf: ConnectionConf, spec: CollectionSpec):
    cluster = get_cluster(conf)
    bucket = cluster.bucket(spec.bucket)
    manager = bucket.collections()

    try:
        manager.create_collection(
            collections.CollectionSpec(spec.name, spec.scope, spec.max_expiry)
        )
        logger.info(f"Collection {log.blue(spec.name)} created.")
    except CollectionAlreadyExistsException:
        pass

@validate_arguments
def exec(conf: ConnectionConf, query: str, *args, **kwargs) -> Dict[str, Any]:
    log_str = "Running command {} ({}, {}) against {}".format(
        log.blue(query),
        log.white(json.dumps(args)),
        log.white(json.dumps(kwargs)),
        log.magenta(conf.url),
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
    (get_cluster(config)
     .bucket(spec.bucket)
     .scope(spec.scope)
     .collection(spec.collection)
     .insert(spec.key, spec.data))

@validate_arguments
def ensure_collection_primary_index_exists(conf: ConnectionConf, spec: CollectionSpec):
    try:
        exec(conf,
             f'CREATE PRIMARY INDEX ON `{spec.bucket}`.`{spec.scope}`.`{spec.name}`')
    except QueryIndexAlreadyExistsException:
        pass

## Migrations ##

@validate_arguments
def init_migration_collection(conf: ConnectionConf):
    ensure_bucket_exists(conf, {'name': MIGRATIONS_BUCKET,
                                'ram_quota_mb': 100,
                                'bucket_type': BucketType.COUCHBASE})
    collection = {'name': MIGRATIONS_COLLECTION, 'bucket': MIGRATIONS_BUCKET}
    ensure_collection_exists(conf, collection)
    ensure_collection_primary_index_exists(conf, collection)

@validate_arguments
def record(conf: ConnectionConf, migration_id: str):
    insert(conf, {'bucket': MIGRATIONS_BUCKET,
                  'collection': MIGRATIONS_COLLECTION,
                  'key': migration_id,
                  'data': {"ts": datetime.utcnow().isoformat(), "id": migration_id}})

@validate_arguments
def list_recorded(conf: ConnectionConf) -> list[MigrationRecord]:
    return exec(conf,
                "SELECT {c}.* FROM `{b}`.`_default`.`{c}`".format(
                    b=MIGRATIONS_BUCKET,
                    c=MIGRATIONS_COLLECTION
                ))
