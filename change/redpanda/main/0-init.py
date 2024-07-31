from kafka.admin import KafkaAdminClient, NewTopic
from typic import Dict

def change(connection_settings: Dict, env_id: str):
    admin_client = KafkaAdminClient(**connection_settings)

    num_partions_per_env = {
        'production': 3,
        'stage': 1,

    topic = NewTopic(name='item_changes', num_partitions=1, replication_factor=1)
    admin_client.create_topics([topic])
    admin_client.close()

