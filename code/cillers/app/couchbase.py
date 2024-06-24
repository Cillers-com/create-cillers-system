import json
import time
from datetime import timedelta
from typing import Annotated, Any, Dict
import logging
import urllib.request
import urllib.parse
import json

from couchbase.auth import PasswordAuthenticator
from couchbase.diagnostics import ServiceType
from couchbase.options import WaitUntilReadyOptions
from couchbase.exceptions import CouchbaseException
from couchbase.options import ClusterOptions, QueryOptions
from couchbase.cluster import Cluster
from couchbase.management.buckets import BucketSettings, BucketType
from couchbase.management.collections import CollectionManager

from pydantic import BaseModel, StringConstraints, validate_arguments
from pydantic.networks import Url, UrlConstraints

logger = logging.getLogger(__name__)

CouchbaseUrl = Annotated[
    Url,
    UrlConstraints(max_length=2083, allowed_schemes=["couchbase", "couchbases"]),
]

Username = Annotated[str, StringConstraints(pattern=r'^[a-zA-Z0-9._-]+$')]

class ConnectionConf(BaseModel):
    url: CouchbaseUrl
    username: Username
    password: str

class DocRef(BaseModel):
    bucket: str
    scope: str = '_default'
    collection: str = '_default'
    key: str

class DocSpec(BaseModel):
    key: str
    data: Any
    bucket: str
    scope: str = '_default'
    collection: str = '_default'

def get_cluster(client_conf):
    max_retries = 20
    connection = client_conf['connection']
    credentials = client_conf['credentials']
    connection_string = f"{connection['protocol']}://{connection['host']}"
    auth = PasswordAuthenticator(credentials['username'], credentials['password'])
    for attempt in range(max_retries):
        try:
            cluster = Cluster(connection_string, ClusterOptions(auth))
            return cluster
        except Exception as e:
            if attempt == max_retries - 1:
                raise e 
            print(f"Cluster connection failed. Retrying ... Error: {e}")
            time.sleep(1)
    assert False

def get_collection_manager(cluster, bucket_name):
    max_retries = 20
    for attempt in range(max_retries):
        try:
            collection_manager = cluster.bucket(bucket_name).collections()
            return collection_manager
        except Exception as e:
            if attempt == max_retries - 1: 
                raise e
            print(f"Get collection manager failed. Retrying ... Error: {e}")
            time.sleep(1)
    assert False

    
bucket_type_conf_to_sdk = {
        'couchbase': BucketType.COUCHBASE,
        'memcached': BucketType.MEMCACHED,
        'ephemeral': BucketType.EPHEMERAL
    }

def bucket_needs_update(bucket, bucket_settings):
    if existing_bucket.ram_quota_mb != settings.ram_quota_mb: return True
    if existing_bucket.num_replicas != settings.num_replicas: return True
    if existing_bucket.durability_min_level != settings.durability_min_level: return True
    return False 

def update_bucket(cluster, bucket, settings):
    bucket.ram_quota_mb = settings.ram_quota_mb
    bucket.num_replicas = settings.num_replicas
    bucket.durability_min_level = settings.durability_min_level
    bucket_manager = cluster.buckets()
    bucket_manager.update_bucket(bucket)

def ensure_bucket_provisioned(cluster, settings):
    try:
        bucket_manager = cluster.buckets()
        existing_buckets = bucket_manager.get_all_buckets()
        existing_bucket = next((b for b in existing_buckets if b.name == settings.name), None)

        if existing_bucket:
            print(f"Bucket '{settings.name}' already exists.")
            if bucket_needs_update(existing_bucket, settings):
                update_bucket(existing_bucket, settings) 
                print(f"Updated '{settings.name}' settings to match required specifications.")
        else:
            print(f"Bucket '{settings.name}' does not exist. Creating new bucket...")
            bucket_manager.create_bucket(settings)
            
    except Exception as e:
        print(f"An error occurred: {e}")
        raise

def ensure_scope_exists(cluster, bucket_name, scope_name):
    collection_manager = get_collection_manager(cluster, bucket_name)
    scopes = collection_manager.get_all_scopes()
    scope_names = [scope.name for scope in scopes]
    if scope_name not in scope_names:
        collection_manager.create_scope(scope_name)
        print(f"Scope '{scope_name}' created in bucket '{bucket_name}'.")
    else:
        print(f"Scope '{scope_name}' already exists in bucket '{bucket_name}'.")

def ensure_cluster_initialized(datastore_conf, cluster_conf, client_conf):
    print(f"Ensuring Couchbase cluster is initialized")
    initialize_cluster(datastore_conf, cluster_conf, client_conf)

def generate_metadata_bucket_settings(datastore_conf, cluster_conf):
    metadata_conf = datastore_conf['metadata']
    metadata_bucket_specs_conf = cluster_conf['metadata_bucket_specs']
    bucket_settings = BucketSettings(
            name = metadata_conf['bucket'],
            bucket_type = BucketType.COUCHBASE,
            ram_quota_mb = metadata_bucket_specs_conf['ram'],
            num_replicas = metadata_bucket_specs_conf['replicas'],
            durability_min_level = metadata_bucket_specs_conf['durability']
        )
    return bucket_settings

def ensure_metadata_initialized(datastore_conf, cluster_conf, client_conf):
    print(f"Ensuring Couchbase cluster metadata is initialized")
    cluster = get_cluster(client_conf)
    bucket_settings = generate_metadata_bucket_settings(datastore_conf, cluster_conf)
    ensure_bucket_provisioned(cluster, bucket_settings)
    ensure_scope_exists(cluster, bucket_settings.name, 'metadata')

def wait_until_ready_for_instructions(client_conf, max_retries=100, retry_delay=1, timeout_seconds=10):
    print("Connecting to Couchbase ...")
    service_types = [
            ServiceType.Management,
            ServiceType.KeyValue,
            ServiceType.Query
        ]
    timeout_option = timedelta(seconds=timeout_seconds)
    wait_until_ready_options = WaitUntilReadyOptions(service_types=service_types)
    for attempt in range(max_retries):
        try:
            cluster = get_cluster(client_conf)
            cluster.wait_until_ready(timeout_option, wait_until_ready_options)
            print("Couchbase is ready for instructions.")
            return
        except Exception as e:
            print(f"Retrying... {e}")
            time.sleep(retry_delay)
    raise Exception("Failed to connnect to Couchbase.")

def is_cluster_initialized(client_conf):
    max_retries = 30
    for attempt in range(max_retries):
        try:
            # If we can connect with credentials, the cluster has been initialized
            cluster = get_cluster(client_conf)
            cluster.buckets().get_all_buckets() 
            return True
        except CouchbaseException as e:
            message = str(e)
            if 'message=request_canceled' in message:
                print("Cluster connection request was cancelled, retrying ...")
                time.sleep(1)
            elif 'message=authentication_failure' in message:
                print("Failed to connect with credentials. We assume the cluster has not been initialized")
                return False
    raise Exception("Max retries exceeded")

def ensure_bucket_exists(bucket_conf):
    # Create a manager instance to interact with the cluster
    cluster_manager = cluster.buckets()
    
    # Get the list of buckets
    bucket_list = cluster_manager.get_all_buckets()
    
    # Check if the specified bucket exists
    exists = any(bucket.name == bucket_name for bucket in bucket_list)
    return exists

def initialize_cluster_test():
    url = "http://couchbase:8091/clusterInit"
    data = {
        'username': 'admin',
        'password': 'password',
        'services': 'kv,n1ql,index,fts,cbas,eventing,backup',
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
    try:
        response = urllib.request.urlopen(request)
        response_body = response.read().decode()
        print("Cluster initialization successful.")
    except urllib.error.URLError as e:
        error_message = str(e)
        print(e)
        if 'already initialized' in error_message:
            print("Cluster was already initialized.")
        else:
            raise Exception(f"Failed to initialize cluster: {e}")

def initialize_cluster(datastore_conf, cluster_conf, client_conf):
    connection = client_conf['connection']
    credentials = client_conf['credentials']
    specs = cluster_conf['specs']
    url = f"http://{connection['host']}:8091/clusterInit"
    data = {
        'username': credentials['username'],
        'password': credentials['password'],
        'services': 'kv', #','.join(datastore_conf['services']),
        'hostname': '127.0.0.1',
        'memoryQuota': '256',
        'sendStats': 'false',
        'clusterName': 'cillers',
        'setDefaultMemQuotas': 'true',
        'indexerStorageMode': 'plasma',
        'port': 'SAME'
    }
    print(url)
    print(data)
    # 'kv,n1ql,index,fts,cbas,eventing,backup',
#    if 'data' in datastore_conf['services']:
#        data['memoryQuota'] = specs['ram']
#    if 'index' in datastore_conf['services']:
#        data['indexMemoryQuota'] = specs['index_ram']
#    if 'fts' in datastore_conf['services']:
#        data['ftsMemoryQuota'] = specs['fts_ram']
    encoded_data = urllib.parse.urlencode(data).encode()
    request = urllib.request.Request(url, data=encoded_data, method='POST')
    max_retries = 30
    for attempt in range(max_retries):
        try:
            response = urllib.request.urlopen(request)
            response_body = response.read().decode()
            print("Cluster initialization successful.")
            return
        except Exception as e:
            if attempt == max_retries - 1:
                print('Max retries exceeded')
                raise e
            error_message = str(e)
            if 'already initialized' in error_message:
                print("Cluster was already initialized.")
                return
            elif any(s in error_message for s in ['Broken pipe', 'Connection reset by peer']):
                print(f"The cluster is not responding. Retrying ... {e}")
                time.sleep(1)
    assert False

@validate_arguments
def get_authenticator(conf: ConnectionConf) -> PasswordAuthenticator:
    return PasswordAuthenticator(conf.username, conf.password)

#@validate_arguments
#def get_cluster(conf: ConnectionConf, timeout_s=5) -> Cluster:
#    cluster = Cluster(str(conf.url), ClusterOptions(get_authenticator(conf)))
#    cluster.wait_until_ready(timedelta(seconds=5))
#    return cluster

#### Operations ####

@validate_arguments
def exec(conf: ConnectionConf, query: str, *args, **kwargs) -> Dict[str, Any]:
    log_str = "Running command {} ({}, {}) against {}".format(
        query, json.dumps(args), json.dumps(kwargs), conf.url
    )
    logger.debug(log_str)
    try:
        cluster = get_cluster(conf)

        result = cluster.query(query, QueryOptions(*args, **kwargs)).rows()
        result_list = list(result)

        logger.trace(f"{log_str} – got {result_list}")
        return result_list

    except CouchbaseException as e:
        logger.error(f"Couchbase error: {e}")
        raise

@validate_arguments
def insert(conf: ConnectionConf, spec: DocSpec) -> Dict[str, Any]:
    return (get_cluster(conf)
     .bucket(spec.bucket)
     .scope(spec.scope)
     .collection(spec.collection)
     .insert(spec.key, spec.data))

@validate_arguments
def remove(conf: ConnectionConf, ref: DocRef) -> Dict[str, Any]:
    return (get_cluster(conf)
     .bucket(ref.bucket)
     .scope(ref.scope)
     .collection(ref.collection)
     .remove(ref.key))

@validate_arguments
def get(conf: ConnectionConf, ref: DocRef) -> Dict[str, Any]:
    return (get_cluster(conf)
     .bucket(ref.bucket)
     .scope(ref.scope)
     .collection(ref.collection)
     .get(ref.key))
