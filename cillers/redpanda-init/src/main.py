import os
import sys
from kafka.admin import KafkaAdminClient, NewTopic
from kafka.errors import TopicAlreadyExistsError

def get_env_var(name):
    try:
        return os.environ[name]
    except KeyError:
        raise KeyError(f"Environment variable '{name}' is not set")

REDPANDA_BOOTSTRAP_SERVERS = get_env_var('REDPANDA_BOOTSTRAP_SERVERS')

data_structure_spec = {"topics": ["items"]}

def create_topics(admin_client, topics):
    new_topics = [NewTopic(name=topic, num_partitions=1, replication_factor=1) for topic in topics]
    try:
        admin_client.create_topics(new_topics)
        print(f"Successfully created topics: {topics}")
    except TopicAlreadyExistsError:
        print(f"Topics already exist: {topics}")
    except Exception as e:
        print(f"Failed to create topics: {e}")
        return False
    return True

def app():
    admin_client = KafkaAdminClient(bootstrap_servers=REDPANDA_BOOTSTRAP_SERVERS.split(','))
    
    if not create_topics(admin_client, data_structure_spec["topics"]):
        return False
    
    return True

def main():
    if not app():
        sys.exit(1)
    sys.exit(0)

if __name__ == "__main__":
    main()
