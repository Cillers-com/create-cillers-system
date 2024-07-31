import urllib
import time
from pathlib import Path
from couchbase.cluster import Cluster
from . import bucket, connection, scope, collection
from ..cluster_config import CouchbaseClusterConfig

def ensure_change_directory_exists(data_structure_id: str): 
    change_file_dir = Path('/root/change/couchbase') / data_structure_id 
    change_file_dir.mkdir(parents=True, exist_ok=True)

def ensure_changes_applied_collection_exists(
        cluster: Cluster, conf: CouchbaseClusterConfig, data_structure_id: str):
    keyspace = conf.changes_applied_collection(data_structure_id)
    collection.ensure_exists(cluster, keyspace)

def ensure_change_constructs_initialized(cluster: Cluster, conf: CouchbaseClusterConfig):
    for data_structure_id in conf.data_structures:
        ensure_change_directory_exists(id)
        ensure_changes_applied_collection_exists(cluster, conf, data_structure_id)

def ensure_metadata_initialized(cluster: Cluster, conf: CouchbaseClusterConfig):
    bucket.ensure_provisioned(cluster, conf.metadata_bucket_create)
    scope.ensure_exists(cluster, conf.metadata_bucket_create.name, 'cillers_metadata')
    ensure_change_constructs_initialized(cluster, conf)

def ensure_cluster_initialized(conf: CouchbaseClusterConfig, timeout_seconds: int):
    encoded_data = urllib.parse.urlencode(conf.cluster_init['data']).encode()
    request = urllib.request.Request(conf.cluster_init['url'], data=encoded_data, method='POST')
    max_retries = 30
    for attempt in range(max_retries):
        try:
            response = urllib.request.urlopen(request, timeout=timeout_seconds)
            response_body = response.read().decode()
            print(f"Cluster initialization successful: {response_body}")
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

def ensure_ready_for_change(conf: CouchbaseClusterConfig) -> Cluster:
    ensure_cluster_initialized(conf, 5*60)
    cluster = connection.get_cluster(conf.client_change())
    connection.wait_until_ready_for_change(cluster, 5*60)
    ensure_metadata_initialized(cluster, conf)
    return cluster
