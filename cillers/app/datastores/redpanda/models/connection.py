import time
from kafka.admin import KafkaAdminClient
from kafka.errors import KafkaError

def get_admin_client(client_params: dict) -> KafkaAdminClient:
    max_retries = 20
    for attempt in range(max_retries):
        try:
            return KafkaAdminClient(**client_params)
        except Exception as e:
            if attempt == max_retries - 1:
                raise e
            print(f"Redpanda connection failed. Retrying... Error: {e}")
            time.sleep(1)
    assert False

def wait_until_ready(client: KafkaAdminClient):
    print("Connecting to Redpanda...")
    max_retries = 20
    retry_delay = 1
    for _ in range(max_retries):
        try:
            client.list_topics(timeout=5)
            print("Redpanda is ready.")
            return
        except KafkaError as e:
            print(f"Retrying... {e}")
            time.sleep(retry_delay)
    raise Exception("Failed to connect to Redpanda.")
