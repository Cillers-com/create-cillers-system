import urllib
import time
from pathlib import Path
from kafka import KafkaAdminClient
from config import config
from . import connection, topic

def ensure_ready_for_change(conf: config.ClusterChangeConfig) -> KafkaAdminClient:
    admin_client = connection.get_admin_client(
        conf.connection['host'],
        conf.connection['port'],
        conf.credentials['username'],
        conf.credentials['password'],
        5*60
    )
    connection.wait_until_ready(client, 5*60)
    ensure_metadata_initialized(client, conf)
    return client

def ensure_metadata_initialized(client: RedpandaClient, conf: config.ClusterChangeConfig):
    for key, _ in conf.data_structures.items():
        ensure_change_directory_exists(key)
        ensure_change_topic_exists(client, conf, key)

def ensure_change_directory_exists(key: str): 
    change_file_dir = Path('/root/change/redpanda') / key
    change_file_dir.mkdir(parents=True, exist_ok=True)

def ensure_change_topic_exists(client: RedpandaClient, conf: config.ClusterChangeConfig, key: str):
    topic = NewTopic(
        name=f"cillers_metadata_changes_applied_{key}",
        num_partitions=conf.metadata_topic_specs['num_partitions'],
        replication_factor=conf.metadata_topic_specs['replication_factor']
    )
    topic.ensure_exists(client, topic)

