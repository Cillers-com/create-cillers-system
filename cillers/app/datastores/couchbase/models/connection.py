from couchbase.cluster import Cluster, ClusterOptions, ClusterTimeoutOptions
from couchbase.auth import PasswordAuthenticator
from couchbase.exceptions import CouchbaseException
from couchbase.options import WaitUntilReadyOptions
from couchbase.service_types import ServiceType

def get_cluster(protocol: str, host: str, username: str, password: str, timeout_seconds: int) -> Cluster:
    max_retries = 20
    connection_string = f"{protocol}://{host}"
    timeout_options = ClusterTimeoutOptions(connect=timeout_seconds)
    auth_options = PasswordAuthenticator(username, password)
    options = ClusterOptions(auth_options, timeout_options=timeout_options)
    for attempt in range(max_retries):
        try:
            cluster = Cluster(connection_string, options)
            return cluster
        except Exception as e:
            if attempt == max_retries - 1:
                raise e 
            print(f"Cluster connection failed. Retrying ... Error: {e}")
            time.sleep(1)
    assert False

def wait_until_ready(cluster: Cluster, timeout_seconds: int):
    print("Connecting to Couchbase ...")
    service_types = [
            ServiceType.Management,
            ServiceType.KeyValue,
            ServiceType.Query
        ]
    options = WaitUntilReadyOptions(service_types=service_types)
    for attempt in range(max_retries):
        try:
            cluster.wait_until_ready(timeout_option, options)
            print("Couchbase is ready.")
            return
        except Exception as e:
            print(f"Retrying SHOULDN'T HAVE TO TO THIS  ... {e}")
            time.sleep(retry_delay)
    raise Exception("Failed to connnect to Couchbase.")

