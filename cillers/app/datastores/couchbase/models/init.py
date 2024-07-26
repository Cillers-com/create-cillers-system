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
from . import bucket, connection, scope, collection

def ensure_ready_for_change(conf: config.ClusterChangeConfig):
    ensure_cluster_initialized(conf, 5*60)
    cluster = connection.get_cluster(
        conf.connection['protocol'],
        conf.connection['host'],
        conf.credentials['username'],
        conf.credentials['password'],
        5*60
    )
    connection.wait_until_ready(cluster, 5*60)
    ensure_metadata_initialized(cluster, conf)
    return cluster

def ensure_cluster_initialized(conf: config.ClusterChangeConfig, timeout_seconds: int):
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

def ensure_metadata_initialized(cluster: Cluster, conf: config.ClusterChangeConfig):
    bucket_settings = generate_metadata_bucket_settings(conf)
    bucket.ensure_provisioned(cluster, bucket_settings)
    scope.ensure_exists(cluster, bucket_settings.name, 'cillers_metadata')
    ensure_change_constructs_initialized(cluster, conf)

def generate_metadata_bucket_settings(conf: config.ClusterChangeConfig) -> BucketSettings:
    bucket_settings = BucketSettings(
        name = conf.metadata['bucket'],
        bucket_type = BucketType.COUCHBASE,
        ram_quota_mb = conf.metadata_bucket_specs['ram'],
        num_replicas = conf.metadata_bucket_specs['replicas'],
        durability_min_level = conf.metadata_bucket_specs['durability']
    )
    return bucket_settings

def ensure_change_constructs_initialized(cluster: Cluster, conf: config.ClusterChangeConfig):
    for key, _ in conf.data_structures:
        ensure_change_directory_exists(key)
        ensure_change_collection_exists(cluster, key)

def ensure_change_directory_exists(key: str): 
    change_file_dir = Path('/root/change/couchbase') / key
    change_file_dir.mkdir(parents=True, exist_ok=True)

def ensure_change_collection_exists(cluster: Cluster, conf: config.ClusterChangeConfig, key: str):
    bucket_name = config.metadata['bucket']
    scope_name = config.metadata['scope']
    collection_name = f"changes_applied_{key}"
    collection.ensure_exists(cluster, bucket_name, scope_name, collection_bame)

