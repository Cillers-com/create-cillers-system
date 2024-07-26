import time
from kafka.admin import KafkaAdminClient

def get_admin_client(host: str, port: int, username: str, password: str, timeout_seconds: int) -> KafkaAdminClient:
    max_retries = 20
    bootstrap_servers = [f"{host}:{port}"]
    for attempt in range(max_retries):
        try:
            client = KafkaAdminClient(
                bootstrap_servers=bootstrap_servers,
                client_id=username,
                sasl_mechanism="SCRAM-SHA-256",
                security_protocol="SASL_SSL",
                sasl_plain_username=username,
                sasl_plain_password=password
            )
            return client
        except Exception as e:
            if attempt == max_retries - 1:
                raise e 
            print(f"Redpanda connection failed. Retrying... Error: {e}")
            time.sleep(1)
    assert False

def wait_until_ready(client: RedpandaClient, timeout_seconds: int):
    print("Connecting to Redpanda...")
    max_retries = 20
    retry_delay = 1
    for attempt in range(max_retries):
        try:
            client.metadata(timeout=timeout_seconds)
            print("Redpanda is ready.")
            return
        except RedpandaException as e:
            print(f"Retrying... {e}")
            time.sleep(retry_delay)
    raise Exception("Failed to connect to Redpanda.")

