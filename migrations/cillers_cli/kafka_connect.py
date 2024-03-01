from typing import Annotated, Literal, Optional, Union

from httpx import HTTPStatusError
from pydantic import (
    BaseModel,
    Field,
    StringConstraints,
    root_validator,
    validate_arguments,
)

from . import log
from .http import Client

logger = log.get_logger(__name__)

#### Constants ####

STRING_CONVERTER = 'org.apache.kafka.connect.storage.StringConverter'
JSON_CONVERTER = 'org.apache.kafka.connect.json.JsonConverter'
CB_RAW_JSON_HANDLER = 'com.couchbase.connect.kafka.handler.source.RawJsonSourceHandler'
BYTE_ARRAY_CONVERTER = 'org.apache.kafka.connect.converters.ByteArrayConverter'

#### Types ####

BaseUrl = Annotated[
    str,
    StringConstraints(pattern=r"^https?://[a-zA-Z0-9.-]+:[\d]*(/[a-zA-Z-_.])*$")
]

class ConnectionConf(BaseModel):
    base_url: BaseUrl

class ConnectorConfigBase(BaseModel):
    config_action_reload: str = Field(alias='config.action.reload', default=None)
    connector_class: str = Field(alias='connector.class')
    key_converter: str = Field(alias='key.converter')
    value_converter: str = Field(alias='value.converter')

    errors_log_enable: bool = Field(alias='errors.log.enable', default=None)
    errors_log_include_messages: bool = Field(alias='errors.log.include.messages',
                                              default=None)
    errors_retry_delay_max_ms: int = Field(alias='errors.retry.delay.max.ms',
                                           default=None)
    errors_retry_timeout: int = Field(alias='errors.retry.timeout', default=None)
    errors_tolerance: str = Field(alias='errors.tolerance', default=None)
    header_converter: str = Field(alias='header.converter', default=None)
    predicates: str = Field(alias='predicates', default=None)
    tasks_max: int = Field(alias='tasks.max', default=None)
    transforms: str = Field(alias='transforms', default=None)

    class Config:
        populate_by_name = True

class SinkConnectorConfigBase(ConnectorConfigBase):
    errors_deadletterqueue_context_headers_enable: bool = Field(
        alias='errors.deadletterqueue.context.headers.enable',
        default=None
    )
    errors_deadletterqueue_topic_name: str = Field(
        alias='errors.deadletterqueue.topic.name',
        default=None
    )
    errors_deadletterqueue_topic_replication_factor: int = Field(
        alias='errors.deadletterqueue.topic.replication.factor',
        default=None
    )
    topics: str = Field(alias='topics', default=None)
    topics_regex: str = Field(alias='topics_regex', default=None)

    @root_validator(pre=True)
    def check_keys(cls, values):
        if values.get('topics') is None == values.get('topics_regex') is None:
            raise ValueError('Exactly one of topics or topics_regex must be provided')
        return values

class SourceConnectorConfigBase(ConnectorConfigBase):
    exactly_once_support: str = Field(alias='exactly.once.support', default=None)
    offsets_storage_topic: str = Field(alias='offsets.storage.topic', default=None)
    topic_creation_groups: str = Field(alias='topic.creation.groups', default=None)
    transaction_boundary: str = Field(alias='transaction.boundary', default=None)
    transaction_boundary_interval_ms: int = Field(
        alias='transaction.boundary.interval.ms',
        default=None
    )

class CouchbaseConnectorConfigBase(BaseModel):
    couchbase_bootstrap_timeout: str = Field(alias='couchbase.bootstrap.timeout',
                                             default=None)
    couchbase_bucket: str = Field(alias='couchbase.bucket')
    couchbase_client_certificate_password: str = Field(
        alias='couchbase.client.certificate.password',
        default=None
    )
    couchbase_client_certificate_path: str = Field(
        alias='couchbase.client.certificate.path',
        default=None
    )
    couchbase_enable_hostname_verification: bool = Field(
        alias='couchbase.enable.hostname.verification',
        default=None
    )
    couchbase_enable_tls: bool = Field(alias='couchbase.enable.tls', default=None)
    couchbase_log_document_lifecycle: str = Field(
        alias='couchbase.log.document.lifecycle',
        default=None
    )
    couchbase_log_redaction: str = Field(alias='couchbase.log.redaction', default=None)
    couchbase_network: str = Field(alias='couchbase.network', default=None)
    couchbase_password: str = Field(alias='couchbase.password') # TODO: figure out how to inject
    couchbase_seed_nodes: str = Field(alias='couchbase.seed.nodes')
    couchbase_trust_certificate_path: str = Field(
        alias='couchbase.trust.certificate.path',
        default=None
    )
    couchbase_trust_store_password: str = Field(alias='couchbase.trust.store.password',
                                                default=None)
    couchbase_trust_store_path: str = Field(alias='couchbase.trust.store.path',
                                            default=None)
    couchbase_username: str = Field(alias='couchbase.username')

class CouchbaseSinkConfig(SinkConnectorConfigBase, CouchbaseConnectorConfigBase):
    connector_class: Literal['com.couchbase.connect.kafka.CouchbaseSinkConnector'] \
        = Field(alias='connector.class',
                default='com.couchbase.connect.kafka.CouchbaseSinkConnector')
    couchbase_analytics_max_records_in_batch: int = Field(
        alias='couchbase.analytics.max.records.in.batch',
        default=None
    )
    couchbase_default_collection: str = Field(alias='couchbase.default.collection',
                                              default=None)
    couchbase_document_expiration: str = Field(alias='couchbase.document.expiration',
                                     default=None)
    couchbase_document_id: str = Field(alias='couchbase.document.id', default=None)
    couchbase_document_mode: str = Field(alias='couchbase.document.mode', default=None)
    couchbase_durability: str = Field(alias='couchbase.durability', default=None)
    couchbase_n1ql_create_document: bool = Field(alias='couchbase.n1ql.create.document',
                                      default=None)
    couchbase_n1ql_operation: str = Field(alias='couchbase.n1ql.operation',
                                          default=None)
    couchbase_n1ql_where_fields: str = Field(alias='couchbase.n1ql.where.fields',
                                             default=None)
    couchbase_persist_to: str = Field(alias='couchbase.persist.to', default=None)
    couchbase_remove_document_id: bool = Field(alias='couchbase.remove.document.id',
                                               default=None)
    couchbase_replicate_to: str = Field(alias='couchbase.replicate.to', default=None)
    couchbase_retry_timeout: str = Field(alias='couchbase.retry.timeout', default=None)
    couchbase_sink_handler: str = Field(alias='couchbase.sink.handler', default=None)
    couchbase_subdocument_create_document: bool = Field(
        alias='couchbase.subdocument.create.document',
        default=None
    )
    couchbase_subdocument_create_path: bool = Field(
        alias='couchbase.subdocument.create.path',
        default=None
    )
    couchbase_subdocument_operation: str = Field(
        alias='couchbase.subdocument.operation',
        default=None
    )
    couchbase_subdocument_path: str = Field(
        alias='couchbase.subdocument.path',
        default=None
    )
    couchbase_topic_to_collection: str = Field(
        alias='couchbase.topic.to.collection',
        default=None
    )

class CouchbaseSourceConfig(SourceConnectorConfigBase, CouchbaseConnectorConfigBase):
    connector_class: Literal['com.couchbase.connect.kafka.CouchbaseSourceConnector'] \
        = Field(alias='connector.class',
                default='com.couchbase.connect.kafka.CouchbaseSourceConnector')

    couchbase_batch_size_max: str = Field(alias='couchbase.batch.size.max',
                                          default=None)
    couchbase_black_hole_topic: str = Field(alias='couchbase.black.hole.topic',
                                            default=None)
    couchbase_collection_to_topic: str = Field(alias='couchbase.collection.to.topic',
                                               default=None)
    couchbase_collections: str = Field(alias='couchbase.collections', default=None)
    couchbase_compression: str = Field(alias='couchbase.compression', default=None)
    couchbase_connector_name_in_offsets: str = Field(
        alias='couchbase.connector.name.in.offsets',
        default=None
    )
    couchbase_dcp_trace_document_id_regex: str = Field(
        alias='couchbase.dcp.trace.document.id.regex',
        default=None
    )
    couchbase_enable_dcp_trace: str = Field(alias='couchbase.enable.dcp.trace',
                                            default=None)
    couchbase_event_filter: str = Field(alias='couchbase.event.filter', default=None)
    couchbase_flow_control_buffer: str = Field(alias='couchbase.flow.control.buffer',
                                               default=None)
    couchbase_no_value: str = Field(alias='couchbase.no.value', default=None)
    couchbase_persistence_polling_interval: str = Field(
        alias='couchbase.persistence.polling.interval',
        default=None
    )
    couchbase_scope: str = Field(alias='couchbase.scope', default=None)
    couchbase_source_handler: str = Field(alias='couchbase.source.handler',
                                          default=None)
    couchbase_stream_from: str = Field(alias='couchbase.stream.from', default=None)
    couchbase_topic: str = Field(alias='couchbase.topic', default=None)
    couchbase_xattrs: str = Field(alias='couchbase.xattrs', default=None)

class HttpSinkConfig(SinkConnectorConfigBase):
    connector_class: Literal['io.confluent.connect.http.HttpSinkConnector'] \
        = Field(alias='connector.class',
                default='io.confluent.connect.http.HttpSinkConnector')
    auth_type: str = Field(alias='auth.type', default=None)
    batch_json_as_array: bool = Field(alias='batch.json.as.array', default=None)
    batch_key_pattern: str = Field(alias='batch.key.pattern', default=None)
    batch_max_size: int = Field(alias='batch.max.size', default=None)
    batch_prefix: str = Field(alias='batch.prefix', default=None)
    batch_separator: str = Field(alias='batch.separator', default=None)
    batch_suffix: str = Field(alias='batch.suffix', default=None)
    behavior_on_error: str = Field(alias='behavior.on.error', default=None)
    behavior_on_null_values: str = Field(alias='behavior.on.null.values', default=None)
    confluent_license: str = Field(alias='confluent.license', default=None)
    confluent_topic: str = Field(alias='confluent.topic', default=None)
    confluent_topic_bootstrap_servers: str = Field(
        alias='confluent.topic.bootstrap.servers',
        default=None
    )
    confluent_topic_replication_factor: int = Field(
        alias='confluent.topic.replication.factor',
        default=None
    )
    confluent_topic_security_protocol: str = Field(
        alias='confluent.topic.security.protocol',
        default=None
    )
    confluent_topic_ssl_key_password: str = Field(
        alias='confluent.topic.ssl.key.password',
        default=None
    )
    confluent_topic_ssl_keystore_location: str = Field(
        alias='confluent.topic.ssl.keystore.location',
        default=None
    )
    confluent_topic_ssl_keystore_password: str = Field(
        alias='confluent.topic.ssl.keystore.password',
        default=None
    )
    confluent_topic_ssl_truststore_location: str = Field(
        alias='confluent.topic.ssl.truststore.location',
        default=None
    )
    confluent_topic_ssl_truststore_password: str = Field(
        alias='confluent.topic.ssl.truststore.password',
        default=None
    )
    connection_password: str = Field(alias='connection.password', default=None)
    connection_user: str = Field(alias='connection.user', default=None)
    headers: str = Field(alias='headers', default=None)
    http_api_url: str = Field(alias='http.api.url')
    http_connect_timeout_ms: int = Field(alias='http.connect.timeout.ms', default=None)
    http_proxy_host: str = Field(alias='http.proxy.host', default=None)
    http_proxy_password: str = Field(alias='http.proxy.password', default=None)
    http_proxy_port: int = Field(alias='http.proxy.port', default=None)
    http_proxy_user: str = Field(alias='http.proxy.user', default=None)
    http_request_timeout_ms: int = Field(alias='http.request.timeout.ms', default=None)
    https_ssl_cipher_suites: str = Field(alias='https.ssl.cipher.suites', default=None)
    https_ssl_enabled_protocols: str = Field(alias='https.ssl.enabled.protocols',
                                             default=None)
    https_ssl_endpoint_identification_algorithm: str = Field(
        alias='https.ssl.endpoint.identification.algorithm',
        default=None
    )
    https_ssl_key_password: str = Field(alias='https.ssl.key.password', default=None)
    https_ssl_keymanager_algorithm: str = Field(alias='https.ssl.keymanager.algorithm',
                                                default=None)
    https_ssl_keystore_location: str = Field(alias='https.ssl.keystore.location',
                                             default=None)
    https_ssl_keystore_password: str = Field(alias='https.ssl.keystore.password',
                                             default=None)
    https_ssl_keystore_type: str = Field(alias='https.ssl.keystore.type', default=None)
    https_ssl_protocol: str = Field(alias='https.ssl.protocol', default=None)
    https_ssl_provider: str = Field(alias='https.ssl.provider', default=None)
    https_ssl_secure_random_implementation: str = Field(
        alias='https.ssl.secure.random.implementation',
        default=None
    )
    https_ssl_trustmanager_algorithm: str = Field(
        alias='https.ssl.trustmanager.algorithm',
        default=None
    )
    https_ssl_truststore_location: str = Field(alias='https.ssl.truststore.location',
                                               default=None)
    https_ssl_truststore_password: str = Field(alias='https.ssl.truststore.password',
                                               default=None)
    https_ssl_truststore_type: str = Field(alias='https.ssl.truststore.type',
                                           default=None)
    max_retries: int = Field(alias='max.retries', default=None)
    oauth2_client_auth_mode: str = Field(alias='oauth2.client.auth.mode', default=None)
    oauth2_client_header_separator: str = Field(alias='oauth2.client.header.separator',
                                                default=None)
    oauth2_client_headers: str = Field(alias='oauth2.client.headers', default=None)
    oauth2_client_id: str = Field(alias='oauth2.client.id', default=None)
    oauth2_client_scope: str = Field(alias='oauth2.client.scope', default=None)
    oauth2_client_secret: str = Field(alias='oauth2.client.secret', default=None)
    oauth2_jwt_claimset: str = Field(alias='oauth2.jwt.claimset', default=None)
    oauth2_jwt_enabled: bool = Field(alias='oauth2.jwt.enabled', default=None)
    oauth2_jwt_keystore_password: str = Field(alias='oauth2.jwt.keystore.password',
                                              default=None)
    oauth2_jwt_keystore_path: str = Field(alias='oauth2.jwt.keystore.path',
                                          default=None)
    oauth2_jwt_keystore_type: str = Field(alias='oauth2.jwt.keystore.type',
                                          default=None)
    oauth2_jwt_signature_algorithm: str = Field(alias='oauth2.jwt.signature.algorithm',
                                                default=None)
    oauth2_token_property: str = Field(alias='oauth2.token.property', default=None)
    oauth2_token_url: str = Field(alias='oauth2.token.url', default=None)
    regex_patterns: str = Field(alias='regex.patterns', default=None)
    regex_replacements: str = Field(alias='regex.replacements', default=None)
    regex_separator: str = Field(alias='regex.separator', default=None)
    report_errors_as: str = Field(alias='report.errors.as', default=None)
    reporter_bootstrap_servers: str = Field(alias='reporter.bootstrap.servers',
                                            default=None)
    reporter_error_topic_key_format: str = Field(
        alias='reporter.error.topic.key.format',
        default=None
    )
    reporter_error_topic_key_format_schemas_cache_size: int = Field(
        alias='reporter.error.topic.key.format.schemas.cache.size',
        default=None
    )
    reporter_error_topic_key_format_schemas_enable: bool = Field(
        alias='reporter.error.topic.key.format.schemas.enable',
        default=None
    )
    reporter_error_topic_name: str = Field(alias='reporter.error.topic.name',
                                           default=None)
    reporter_error_topic_partitions: str = Field(
        alias='reporter.error.topic.partitions',
        default=None
    )
    reporter_error_topic_replication_factor: int = Field(
        alias='reporter.error.topic.replication.factor',
        default=None
    )
    reporter_error_topic_value_format: str = Field(
        alias='reporter.error.topic.value.format',
        default=None
    )
    reporter_error_topic_value_format_schemas_cache_size: int = Field(
        alias='reporter.error.topic.value.format.schemas.cache.size',
        default=None
    )
    reporter_error_topic_value_format_schemas_enable: bool = Field(
        alias='reporter.error.topic.value.format.schemas.enable',
        default=None
    )
    reporter_result_topic_key_format: str = Field(
        alias='reporter.result.topic.key.format',
        default=None
    )
    reporter_result_topic_key_format_schemas_cache_size: int = Field(
        alias='reporter.result.topic.key.format.schemas.cache.size',
        default=None
    )
    reporter_result_topic_key_format_schemas_enable: bool = Field(
        alias='reporter.result.topic.key.format.schemas.enable',
        default=None
    )
    reporter_result_topic_name: str = Field(alias='reporter.result.topic.name',
                                            default=None)
    reporter_result_topic_partitions: str = Field(
        alias='reporter.result.topic.partitions',
        default=None
    )
    reporter_result_topic_replication_factor: int = Field(
        alias='reporter.result.topic.replication.factor',
        default=None
    )
    reporter_result_topic_value_format: str = Field(
        alias='reporter.result.topic.value.format',
        default=None
    )
    reporter_result_topic_value_format_schemas_cache_size: int = Field(
        alias='reporter.result.topic.value.format.schemas.cache.size',
        default=None
    )
    reporter_result_topic_value_format_schemas_enable: bool = Field(
        alias='reporter.result.topic.value.format.schemas.enable',
        default=None
    )
    request_body_format: str = Field(alias='request.body.format', default=None)
    request_method: str = Field(alias='request.method', default=None)
    retry_backoff_ms: int = Field(alias='retry.backoff.ms', default=None)
    retry_on_status_codes: str = Field(alias='retry.on.status.codes', default=None)


ConnectorConfig = Annotated[Union[CouchbaseSinkConfig,
                                  CouchbaseSourceConfig,
                                  HttpSinkConfig],
                            Field(discriminator='connector_class')]

class ConnectorSpec(BaseModel):
    name: str
    config: ConnectorConfig

    class Config:
        populate_by_name = True

#### Utils ####

## Paths ##

def connectors_path(base_url: str) -> str:
    return f"{base_url}/connectors"

def connector_path(base_url: str, connector: str) -> str:
    return f"{connectors_path(base_url)}/{connector}"

def config_path(base_url: str, connector: str) -> str:
    return f"{connector_path(base_url, connector)}/config"

#### Operations ####

@validate_arguments
def list_connectors(conf: ConnectionConf) -> [str]:
    with Client() as client:
        resp = client.get(connectors_path(conf.base_url))
        resp.raise_for_status()
        return resp.json()

@validate_arguments
def get_connector(conf: ConnectionConf, connector: str) -> Optional[ConnectorSpec]:
    with Client() as client:
        try:
            resp = client.get(connector_path(conf.base_url, connector))
            resp.raise_for_status()
            return resp.json()
        except HTTPStatusError as e:
            if e.response.status_code == 404:
                return None
            raise

@validate_arguments
def create_connector(conf: ConnectionConf, spec: ConnectorSpec) -> ConnectorSpec:
    with Client() as client:
        resp = client.post(connectors_path(conf.base_url),
                           json=spec.dict(by_alias=True, exclude_none=True))
        resp.raise_for_status()
    return get_connector(conf, spec.name)

@validate_arguments
def update_connector(conf: ConnectionConf, spec: ConnectorSpec) -> ConnectorSpec:
    with Client() as client:
        curr = get_connector(conf, spec.name)['config']
        diff = {}
        config = spec.config.dict(by_alias=True, exclude_none=True)
        for k, v in config.items():
            if v:
                if isinstance(v, bool):
                    v = 'true' if v else 'false'
                else:
                    v = str(v)
            old = curr.get(k)
            if old != v:
                diff[k] = {'old': old, 'new': v}
        if diff:
            logger.info('Applying diff to connector %s: %s',
                        log.blue(spec.name), diff)
            resp = client.put(config_path(conf.base_url, spec.name),
                              json={**curr, **config})
            resp.raise_for_status()
    return get_connector(conf, spec.name)

@validate_arguments
def delete_connector(conf: ConnectionConf, connector: str) -> None:
    with Client() as client:
        try:
            resp = client.delete(connector_path(conf.base_url, connector))
            resp.raise_for_status()
            logger.info(f"Connector {connector} deleted.")
        except HTTPStatusError as e:
            if e.response.status_code == 404:
                return None
            raise

@validate_arguments
def ensure_connector_exists(conf: ConnectionConf, spec: ConnectorSpec) -> ConnectorSpec:
    with Client() as client:
        resp = client.post(connectors_path(conf.base_url),
                           json=spec.dict(by_alias=True, exclude_none=True))
        if resp.status_code == 409:
            return update_connector(conf, spec)
        else:
            resp.raise_for_status()
            logger.info(f"Connector {log.blue(spec.name)} created.")
