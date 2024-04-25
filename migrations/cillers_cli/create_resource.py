from datetime import datetime

from pydantic import validate_arguments
from pathlib import Path
from pydantic import BaseModel
from pydantic.networks import Url

from . import fs, log
from .types import (
    CreateConnectorOp,
    CreateCollectionOp,
    CreateTopicOp,
    CreateBucketOp,
    Migration,
    ConnectionConfs
)
from .couchbase import CollectionSpec, BucketSpec
from .kafka_connect import (
    CouchbaseSinkConfig,
    CouchbaseSourceConfig,
    ConnectorSpec,
    HttpSinkConfig,
    STRING_CONVERTER,
    JSON_CONVERTER,
    BYTE_ARRAY_CONVERTER,
    CB_RAW_JSON_HANDLER
)
from .kafka import TopicSpec

logger = log.get_logger(__name__)

class ResourceSpec(BaseModel):
    name: str
    bucket: str
    sink_url: Url | None = None

@validate_arguments
def get_migration(configs: ConnectionConfs, spec: ResourceSpec) -> Migration:
    bucket = spec.bucket
    name = spec.name
    migration_id = f'{datetime.now().strftime("%Y-%m-%d")}-{name}'
    ops = [
        CreateBucketOp(spec=BucketSpec(name=bucket,
                                       bucket_type='membase',
                                       ram_quota_mb=100)),
        CreateTopicOp(spec=TopicSpec(name=f'{name}-in',
                                     num_partitions=1,
                                     replication_factor=1)),
        CreateCollectionOp(spec=CollectionSpec(name=name, bucket=bucket)),
        CreateConnectorOp(
            spec=ConnectorSpec(
                name=f'{name}-couchbase-sink',
                config=CouchbaseSinkConfig(
                    couchbase_bucket=bucket,
                    couchbase_default_collection=f'_default.{name}',
                    couchbase_password='password',
                    couchbase_seed_nodes='couchbase',
                    couchbase_username='admin',
                    key_converter=STRING_CONVERTER,
                    name=f'couchbase-sink-{name}',
                    tasks_max=2,
                    topics=f'{name}-in',
                    value_converter=JSON_CONVERTER,
                )
            )
        )
    ]
    if spec.sink_url:
        ops.extend([
            CreateTopicOp(name=f'{name}-out'),
            CreateConnectorOp(
                spec=ConnectorSpec(
                    name=f'{name}-couchbase-source',
                    config=CouchbaseSourceConfig(
                        couchbase_bucket=bucket,
                        couchbase_collections=f'_default.{name}',
                        couchbase_password='password',
                        couchbase_seed_nodes='couchbase',
                        couchbase_source_handler=CB_RAW_JSON_HANDLER,
                        couchbase_topic=f'{name}-out',
                        couchbase_username='admin',
                        key_converter=STRING_CONVERTER,
                        name=f'couchbase-source-{name}',
                        tasks_max=2,
                        value_converter=BYTE_ARRAY_CONVERTER,
                    )
                )
            ),
            CreateConnectorOp(
                spec=ConnectorSpec(
                    name=f'{name}-http-sink',
                    config=HttpSinkConfig(
                        confluent_topic_bootstrap_servers='kafka:9092',
                        confluent_topic_replication_factor=1,
                        connector_class='io.confluent.connect.http.HttpSinkConnector',
                        headers='Content-Type:application/json; charset=UTF-8',
                        http_api_url='http://pastebin_org',
                        key_converter=STRING_CONVERTER,
                        reporter_bootstrap_servers='kafka:9092',
                        reporter_error_topic_name='error-responses',
                        reporter_error_topic_replication_factor=1,
                        reporter_result_topic_name='success-responses',
                        reporter_result_topic_replication_factor=1,
                        tasks_max=1,
                        topics='foo-out',
                        value_converter=STRING_CONVERTER
                    )
                )
            )
        ])
    return Migration(id=migration_id, ops=ops)

@validate_arguments
def create(configs: ConnectionConfs, spec: ResourceSpec, migration_dir: Path):
    fs.validate_migration_dir(migration_dir, write=True)
    bucket = spec.bucket
    name = spec.name
    migration_id = f'{datetime.now().strftime("%Y-%m-%d")}-{name}'
    ops = [
        CreateBucketOp(spec=BucketSpec(name=bucket,
                                       bucket_type='membase',
                                       ram_quota_mb=100)),
        CreateTopicOp(spec=TopicSpec(name=f'{name}-in',
                                     num_partitions=1,
                                     replication_factor=1)),
        CreateCollectionOp(spec=CollectionSpec(name=name, bucket=bucket)),
        CreateConnectorOp(
            spec=ConnectorSpec(
                name=f'{name}-couchbase-sink',
                config=CouchbaseSinkConfig(
                    couchbase_bucket=bucket,
                    couchbase_default_collection=f'_default.{name}',
                    couchbase_password='password',
                    couchbase_seed_nodes='couchbase',
                    couchbase_username='admin',
                    key_converter=STRING_CONVERTER,
                    name=f'couchbase-sink-{name}',
                    tasks_max=2,
                    topics=f'{name}-in',
                    value_converter=JSON_CONVERTER,
                )
            )
        )
    ]
    if spec.sink_url:
        ops.extend([
            CreateTopicOp(spec=TopicSpec(name=f'{name}-out',
                                         num_partitions=1,
                                         replication_factor=1)),
            CreateConnectorOp(
                spec=ConnectorSpec(
                    name=f'{name}-couchbase-source',
                    config=CouchbaseSourceConfig(
                        couchbase_bucket=bucket,
                        couchbase_collections=f'_default.{name}',
                        couchbase_password='password',
                        couchbase_seed_nodes='couchbase',
                        couchbase_source_handler=CB_RAW_JSON_HANDLER,
                        couchbase_topic=f'{name}-out',
                        couchbase_username='admin',
                        key_converter=STRING_CONVERTER,
                        name=f'couchbase-source-{name}',
                        tasks_max=2,
                        value_converter=BYTE_ARRAY_CONVERTER,
                    )
                )
            ),
            CreateConnectorOp(
                spec=ConnectorSpec(
                    name=f'{name}-http-sink',
                    config=HttpSinkConfig(
                        confluent_topic_bootstrap_servers='kafka:9092',
                        confluent_topic_replication_factor=1,
                        connector_class='io.confluent.connect.http.HttpSinkConnector',
                        headers='Content-Type:application/json; charset=UTF-8',
                        http_api_url='http://pastebin_org',
                        key_converter=STRING_CONVERTER,
                        reporter_bootstrap_servers='kafka:9092',
                        reporter_error_topic_name='error-responses',
                        reporter_error_topic_replication_factor=1,
                        reporter_result_topic_name='success-responses',
                        reporter_result_topic_replication_factor=1,
                        tasks_max=1,
                        topics='foo-out',
                        value_converter=STRING_CONVERTER
                    )
                )
            )
        ])
    migration = Migration(id=migration_id, ops=ops)
    fs.write_migration(migration_dir, migration)
