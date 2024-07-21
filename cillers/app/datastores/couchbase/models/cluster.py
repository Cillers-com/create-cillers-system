import urllib
import time
from pathlib import Path
from datetime import timedelta
from couchbase.cluster import Cluster, ClusterOptions, ClusterTimeoutOptions
from couchbase.auth import PasswordAuthenticator
from couchbase.exceptions import CouchbaseException
from couchbase.management.buckets import BucketManager
from couchbase.options import WaitUntilReadyOptions
from couchbase.service_types import ServiceType
from config import config
from . import bucket, metadata

def ensure_ready_for_change(conf: config.ClusterChangeConfig):
    ensure_initialized(conf, 5*60)
    cluster = get(conf, 5*60)
    wait_until_ready(cluster, 5*60)
    metadata.ensure_initialized(cluster, conf)

def ensure_initialized(conf: config.ClusterChangeConfig, timeout_seconds: int):
    url = f"http://{conf.connection['host']}:8091/clusterInit"
    data = {
        'username': conf.credentials['username'],
        'password': conf.credentials['password'],
        'services': ','.join(services),
        'hostname': '127.0.0.1',
        'memoryQuota': '256',
        'sendStats': 'false',
        'clusterName': 'cillers',
        'setDefaultMemQuotas': 'true',
        'indexerStorageMode': 'plasma',
        'port': 'SAME'
    }
    encoded_data = urllib.parse.urlencode(data).encode()
    request = urllib.request.Request(url, data=encoded_data, method='POST')
    max_retries = 30
    for attempt in range(max_retries):
        try:
            response = urllib.request.urlopen(request, timeout=timeout_seconds)
            response_body = response.read().decode()
            print("Cluster initialization successful.")
            return
        except Exception as e:
            if attempt == max_retries - 1:
                print('Max retries exceeded')
                raise e
            error_message = str(e)
            if 'already initialized' in error_message or 'Unauthorized' in error_message:
                print("Cluster was already initialized.")
                return
            else: 
                print(f"The cluster is not responding. Retrying SHOULDN'T HAVE TO DO THIS ... {e}")
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
            cluster = get(conf, timeout_seconds)
            cluster.wait_until_ready(timeout_option, options)
            print("Couchbase is ready.")
            return
        except Exception as e:
            print(f"Retrying SHOULDN'T HAVE TO TO THIS  ... {e}")
            time.sleep(retry_delay)
    raise Exception("Failed to connnect to Couchbase.")

def get(conf: config.ClusterChangeConfig, timeout_seconds: int):
    max_retries = 20
    connection_string = generate_connection_string(conf)
    options = generate_options(conf)
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

def generate_connection_string(conf: config.ClusterChangeConfig) -> str:
    return f"{conf.connection['protocol']}://{conf.connection['host']}"

def generate_options(conf: config.ClusterChangeConfig, timeout_seconds) -> ClusterOptions:
    timeout_options = ClusterTimeoutOptions(connect=timeout_seconds)
    auth_options = PasswordAuthenticator(conf.credentials['username'], conf.credentials['password'])
    return ClusterOptions(auth_options, timeout_options=timeout_options)


#def is_initialized(client_conf):
#    max_retries = 30
#    for attempt in range(max_retries):
#        try:
#            # If we can connect with credentials, the cluster has been initialized
#            cluster = get_cluster(client_conf)
#            cluster.buckets().get_all_buckets() 
#            return True
#        except CouchbaseException as e:
#            message = str(e)
#            if 'message=request_canceled' in message:
#                print("Cluster connection request was cancelled, retrying ...")
#                time.sleep(1)
#            elif 'message=authentication_failure' in message:
#                print("Failed to connect with credentials. We assume the cluster has not been initialized")
#                return False
#    raise Exception("Max retries exceeded")

