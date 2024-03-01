from enum import Enum

from confluent_kafka import KafkaError, KafkaException
from confluent_kafka.admin import (
    AdminClient,
    AlterConfigOpType,
    ConfigEntry,
    ConfigResource,
    NewPartitions,
    NewTopic,
    TopicMetadata,
)
from pydantic import BaseModel, Field, validate_arguments, validator, StringConstraints
from typing import Annotated

from . import log

logger = log.get_logger(__name__)

#### Constants ####

TIMEOUT_S = 5

#### Types ####

## Connection ##

BootstrapServers = Annotated[
    str,
    StringConstraints(pattern=r"^(?:[a-zA-Z0-9.-]+:\d+[,])*[a-zA-Z0-9.-]+:\d+$")
]

class ConnectionConf(BaseModel):
    bootstrap_servers: BootstrapServers = Field(alias='bootstrap.servers')
    client_id: str = Field(alias='client.id', default='cillers-cli')

    class Config:
        populate_by_name = True

## Specs ##

class CleanupPolicy(str, Enum):
    DELETE = "delete"
    COMPACT = "compact"

class CompressionType(str, Enum):
    NONE = "none"
    GZIP = "gzip"
    SNAPPY = "snappy"
    LZ4 = "lz4"
    ZSTD = "zstd"

class TimestampType(str, Enum):
    CREATETIME = "CreateTime"
    LOGAPPENDTIME = "LogAppendTime"

class CleanupConfig(BaseModel):
    policy: CleanupPolicy = None

class CompressionConfig(BaseModel):
    type: CompressionType = None

class ReplicationConfig(BaseModel):
    throttled_replicas: str = None

class MessageConfig(BaseModel):
    format_version: str = None
    timestamp_difference_max_ms: int = None
    timestamp_type: TimestampType = None

class SegmentConfig(BaseModel):
    bytes: int = None
    index_bytes: int = None
    jitter_ms: int = None
    ms: int = None

class RetentionConfig(BaseModel):
    bytes: int = None
    ms: int = None

class TopicConfig(BaseModel):
    cleanup_policy: str = Field(alias='cleanup.policy', default=None)
    compression_type: str = Field(alias='compression.type', default=None)
    confluent_cluster_link_allow_legacy_message_format: bool = Field(
        alias='confluent.cluster.link.allow.legacy.message.format',
        default=None
    )
    confluent_key_schema_validation: bool = Field(
        alias='confluent.key.schema.validation',
        default=None
    )
    confluent_key_subject_name_strategy: str = Field(
        alias='confluent.key.subject.name.strategy',
        default=None
    )
    confluent_placement_constraints: str = Field(
        alias='confluent.placement.constraints',
        default=None
    )
    confluent_tier_enable: bool = Field(alias='confluent.tier.enable', default=None)
    confluent_tier_local_hotset_bytes: int = Field(
        alias='confluent.tier.local.hotset.bytes',
        default=None
    )
    confluent_tier_local_hotset_ms: int = Field(
        alias='confluent.tier.local.hotset.ms',
        default=None
    )
    confluent_value_schema_validation: bool = Field(
        alias='confluent.value.schema.validation',
        default=None
    )
    confluent_value_subject_name_strategy: str = Field(
        alias='confluent.value.subject.name.strategy',
        default=None
    )
    delete_retention_ms: int = Field(alias='delete.retention.ms', default=None)
    file_delete_delay_ms: int = Field(alias='file.delete.delay.ms', default=None)
    flush_messages: str = Field(alias='flush.messages', default=None)
    flush_ms: int = Field(alias='flush.ms', default=None)
    follower_replication_throttled_replicas: str = Field(
        alias='follower.replication.throttled.replicas',
        default=None
    )
    index_interval_bytes: int = Field(alias='index.interval.bytes', default=None)
    leader_replication_throttled_replicas: str = Field(
        alias='leader.replication.throttled.replicas',
        default=None
    )
    max_compaction_lag_ms: int = Field(alias='max.compaction.lag.ms', default=None)
    max_message_bytes: int = Field(alias='max.message.bytes', default=None)
    message_downconversion_enable: bool = Field(alias='message.downconversion.enable',
                                                default=None)
    message_format_version: str = Field(alias='message.format.version', default=None)
    message_timestamp_difference_max_ms: int = Field(
        alias='message.timestamp.difference.max.ms',
        default=None
    )
    message_timestamp_type: str = Field(alias='message.timestamp.type', default=None)
    min_cleanable_dirty_ratio: float = Field(
        alias='min.cleanable.dirty.ratio',
        default=None
    )
    min_compaction_lag_ms: int = Field(alias='min.compaction.lag.ms', default=None)
    min_insync_replicas: int = Field(alias='min.insync.replicas', default=None)
    preallocate: bool = Field(alias='preallocate', default=None)
    retention_bytes: int = Field(alias='retention.bytes', default=None)
    retention_ms: int = Field(alias='retention.ms', default=None)
    segment_bytes: int = Field(alias='segment.bytes', default=None)
    segment_index_bytes: int = Field(alias='segment.index.bytes', default=None)
    segment_jitter_ms: int = Field(alias='segment.jitter.ms', default=None)
    segment_ms: int = Field(alias='segment.ms', default=None)
    unclean_leader_election_enable: bool = Field(
        alias='unclean.leader.election.enable',
        default=None
    )


class TopicSpec(BaseModel):
    name: str
    num_partitions: int
    replication_factor: int
    config: TopicConfig | None = None

    @validator("num_partitions", "replication_factor", pre=True, always=True)
    def check_positive(cls, value):
        if value <= 0:
            raise ValueError("Must be a positive integer")
        return value

#### Utils ####

def get_client(conf: ConnectionConf) -> AdminClient:
    # TODO: pass `logger=logger` if it's ever supported for the admin client
    return AdminClient(conf.dict(by_alias=True, exclude_unset=True))

#### Operations ####

@validate_arguments
def create_topic(conf: ConnectionConf, spec: TopicSpec) -> None:
    client = get_client(conf)

    new_topic = NewTopic(spec.name,
                         num_partitions=spec.num_partitions,
                         replication_factor=spec.replication_factor,
                         config=spec.config or {})
    try:
        client.create_topics([new_topic])[spec.name].result(timeout=TIMEOUT_S)
        logger.info(f"Topic {log.blue(spec.name)} created.")
    except KafkaException as e:
        if e.args[0].code() != KafkaError.TOPIC_ALREADY_EXISTS:
            raise e

@validate_arguments
def get_topic(conf: ConnectionConf, topic: str) -> TopicMetadata:
    return (get_client(conf)
            .list_topics(topic=topic, timeout=TIMEOUT_S)
            .topics[topic])

@validate_arguments
def list_topics(conf: ConnectionConf) -> dict[str, TopicMetadata]:
    return get_client(conf).list_topics( timeout=TIMEOUT_S).topics

@validate_arguments
def delete_topic(conf: ConnectionConf, topic_name: str) -> None:
    client = get_client(conf)
    # TODO: check the result (can't do this outside the docker network)
    try:
        client.delete_topics([topic_name])[topic_name].result(timeout=TIMEOUT_S)
        logger.info(f"Deleted topic {topic_name}")
    except KafkaException as e:
        if e.args[0].code() != KafkaError.UNKNOWN_TOPIC_OR_PART:
            raise e

@validate_arguments
def modify_topic(conf: ConnectionConf, spec: TopicSpec) -> None:
    # TODO: support modifying replication factor and number of partitions
    client = get_client(conf)

    md = get_topic(conf, spec.name)
    n_replicas = len(md.partitions[0].replicas)
    if n_replicas != spec.replication_factor:
        raise NotImplementedError(
            "Can't modify replication factor (current count: "
            f"{n_replicas}, requested count: {spec.replication_factor})"
        )

    n_partitions = len(md.partitions)
    if n_partitions != spec.num_partitions:
        if n_partitions > spec.num_partitions:
            raise ValueError("Can't decrease number of partitions (current count: "
                             f"{n_partitions}, requested count: {spec.num_partitions})")
        else:
            op = NewPartitions(spec.name, int(spec.num_partitions))
            client.create_partitions([op])[spec.name].result(timeout=TIMEOUT_S)

    resource = ConfigResource(ConfigResource.Type.TOPIC, spec.name)
    curr = client.describe_configs([resource])[resource].result(timeout=TIMEOUT_S)
    diff = {}
    if spec.config:
        for k, v in spec.config.dict(by_alias=True, exclude_unset=True).items():
            if v:
                if isinstance(v, bool):
                    v = 'true' if v else 'false'
                else:
                    v = str(v)
            old = curr[k].value
            if old != v:
                diff[k] = {'new': v, 'old': old}
        if diff:
            logger.info(f"Modifying topic {spec.name} with config {diff}")
            ops = [ConfigEntry(k,
                               v['new'],
                               incremental_operation=AlterConfigOpType.SET)
                   for k, v in diff.items()]
            r = ConfigResource(resource.restype,
                               resource.name,
                               incremental_configs=ops)
            client.incremental_alter_configs([r])[r].result(timeout=5)

@validate_arguments
def ensure_topic_exists(conf: ConnectionConf, spec: TopicSpec) -> None:
    if spec.name not in list_topics(conf):
        create_topic(conf, spec)
    else:
        modify_topic(conf, spec)
