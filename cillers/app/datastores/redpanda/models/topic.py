from kafka import KafkaAdminClient, NewTopic

def ensure_exists(admin_client: KafkaAdminClient, topic: NewTopic):
    if not exists(admin_client, topic.name):
        create(admin_client, topic)

def exists(client: KafkaAdminClient, topic_name: str) -> bool:
    topic_list = admin_client.list_topics()
    return topic_name in topic_list

def create(client: KafkaAdminClient, topic: NewTopic):
    try:
        client.create_topics([topic])
        print(f"Topic '{topic_name}' created successfully.")
    except Exception as e:
        raise Exception(f"Failed to create topic '{topic_name}': {e}")

