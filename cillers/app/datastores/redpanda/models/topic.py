from kafka.admin import KafkaAdminClient, NewTopic

def create(client: KafkaAdminClient, topic: NewTopic):
    try:
        client.create_topics([topic])
        print(f"Topic '{topic.name}' created successfully.")
    except Exception as e:
        raise Exception(f"Failed to create topic '{topic.name}': {e}") from e

def exists(client: KafkaAdminClient, topic_name: str) -> bool:
    topic_list = client.list_topics()
    return topic_name in topic_list

def ensure_exists(admin_client: KafkaAdminClient, topic: NewTopic):
    if not exists(admin_client, topic.name):
        create(admin_client, topic)

