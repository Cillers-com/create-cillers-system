import time
from couchbase.cluster import Cluster, ClusterOptions, ClusterTimeoutOptions
from couchbase.auth import PasswordAuthenticator
from couchbase.exceptions import CouchbaseException
from couchbase.options import WaitUntilReadyOptions
from couchbase.diagnostics import ServiceType

def get_cluster(params_client: dict) -> Cluster:
    max_retries = 20
    timeout_options = ClusterTimeoutOptions(connect=5*60)
    auth_options = PasswordAuthenticator(
        params_client['credentials']['username'],
        params_client['credentials']['password'])
    options = ClusterOptions(auth_options, timeout_options=timeout_options)
    for attempt in range(max_retries):
        try:
            cluster = Cluster(params_client['connection_string'], options)
            return cluster
        except Exception as e:
            if attempt == max_retries - 1:
                raise e
            print(f"Cluster connection failed. Retrying ... Error: {e}")
            time.sleep(1)
    assert False

def wait_until_ready(cluster: Cluster, service_types: list[ServiceType], timeout_seconds: int):
    print("Waiting until Couchbase is ready ...")
    options = WaitUntilReadyOptions(service_types=service_types)
    max_retries = 200
    retry_delay = 1
    for _ in range(max_retries):
        try:
            timeout_options = ClusterTimeoutOptions(connect=timeout_seconds)
            cluster.wait_until_ready(timeout_options, options)
            print("Couchbase is ready.")
            return
        except CouchbaseException as e:
            print(f"Retrying SHOULDN'T HAVE TO TO THIS  ... {e}")
            time.sleep(retry_delay)
    raise Exception("Failed to connnect to Couchbase.")
