from pathlib import Path
from kafka.admin import KafkaAdminClient, NewTopic
from . import connection, topic
from ..cluster_config import RedpandaClusterConfig

def ensure_change_directory_exists(data_structure_id: str):
    change_file_dir = Path('/root/change/redpanda') / data_structure_id
    change_file_dir.mkdir(parents=True, exist_ok=True)

def ensure_change_topic_exists(
        client: KafkaAdminClient,
        conf: RedpandaClusterConfig,
        data_structure_id: str):
    new_topic = NewTopic(
        conf.change_applied_topic_name(data_structure_id),
        conf.metadata_topic_specs['num_partitions'],
        conf.metadata_topic_specs['replication_factor'])
    topic.ensure_exists(client, new_topic)

def ensure_metadata_initialized(client: KafkaAdminClient, conf: RedpandaClusterConfig):
    for data_structure_id in conf.data_structures:
        ensure_change_directory_exists(data_structure_id)
        ensure_change_topic_exists(client, conf, data_structure_id)

def ensure_ready_for_change(conf: RedpandaClusterConfig) -> KafkaAdminClient:
    client = connection.get_admin_client({
        **conf.client_params_change,
        'request_timeout_ms': 5*60*1000})
    connection.wait_until_ready(client)
    ensure_metadata_initialized(client, conf)
    return client
