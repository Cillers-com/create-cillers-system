import time
from couchbase.cluster import Cluster, ClusterOptions, ClusterTimeoutOptions
from couchbase.auth import PasswordAuthenticator
from couchbase.exceptions import CouchbaseException
from couchbase.options import WaitUntilReadyOptions
from couchbase.diagnostics import ServiceType

def get_cluster(client_params: dict) -> Cluster:
    max_retries = 20
    timeout_options = ClusterTimeoutOptions(connect=5*60)
    auth_options = PasswordAuthenticator(
        client_params['credentials']['username'], 
        client_params['credentials']['password'])
    options = ClusterOptions(auth_options, timeout_options=timeout_options)
    for attempt in range(max_retries):
        try:
            cluster = Cluster(client_params['connection_string'], options)
            return cluster
        except Exception as e:
            if attempt == max_retries - 1:
                raise e 
            print(f"Cluster connection failed. Retrying ... Error: {e}")
            time.sleep(1)
    assert False

def wait_until_ready_for_change(cluster: Cluster, timeout_seconds: int):
    print("Connecting to Couchbase ...")
    service_types = [
            ServiceType.Management,
            ServiceType.KeyValue,
            ServiceType.Query
        ]
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
