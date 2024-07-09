import time
from confluent_kafka import Producer, KafkaException

def wait_until_ready_for_instructions(client_conf, retries=10, retry_delay=1, timeout=10):
    print("Connecting to Redpanda ...")
    connection = client_conf['connection']
    connection_string = f"{connection['host']}:{connection['port']}"
    conf = {'bootstrap.servers': connection_string}
    producer = Producer(conf)
    attempt = 0

    for attempt in range(retries):
        try:
            metadata = producer.list_topics(timeout=timeout)
            if metadata.topics:
                print("Redpanda is ready for instructions.")
                return
        except KafkaException as e:
            print("Retrying ... {e}")
            time.sleep(retry_delay)
        finally:
            producer.flush()
    
    raise Exception(f"Failed to connect to Redpanda server at {server} after {retries} attempts.")

def ensure_cluster_initialized(datastore_conf, cluster_conf, client_conf):
#    print(f"Ensuring Redpanda cluster is initialized")
#    print(datastore_conf, cluster_conf, client_conf)
    return True

def ensure_metadata_initialized(datastore_conf, cluster_conf, client_conf):
#    print(f"Ensuring Redpanda cluster metadata is initialized")
#    metadata_conf = datastore_conf['metadata']
#    metadata_topics_specs_conf = cluster_conf['metadata_topics_specs']
#    print(metadata_conf)
#    print(metadata_topics_specs_conf)
    return True
