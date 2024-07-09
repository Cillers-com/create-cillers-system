import os
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
            print(f"Get collection manager attempt failed. Retrying ... Error: {e}")
            time.sleep(1)
    assert False

def get_collection(cluster, bucket_name, scope_name, collection_name=None):
    max_retries = 20
    for attempt in range(max_retries):
        try:
            bucket = cluster.bucket(bucket_name)
            scope = bucket.scope(scope_name)
            if collection_name: 
                return scope.collection(collection_name)
            else:
                return scope.default_collection()
        except Exception as e:
            if attempt == max_retries - 1: 
                raise e
            print(f"Get collection attempt failed. Retrying ... Error: {e}")
            time.sleep(1)
    assert False

bucket_type_conf_to_sdk = {
        'couchbase': BucketType.COUCHBASE,
        'memcached': BucketType.MEMCACHED,
        'ephemeral': BucketType.EPHEMERAL
    }

def bucket_needs_update(existing_bucket, spec_settings):
    if existing_bucket.get('ram_quota_mb') != spec_settings.get('ramQuotaMB'): return True
    if existing_bucket.numReplicas != spec_settings.numReplicas: return True
    if existing_bucket.durabilityMinLevel != spec_settings.durabilityMinLevel: return True
    return False 

def update_bucket(cluster, bucket, settings):
    bucket.settings.ramQuotaMB = settings.ramQuotaMB
    bucket.settings.numReplicas = settings.numReplicas
    bucket.settings.durabilityMinLevel = settings.durabilityMinLevel
    bucket_manager = cluster.buckets()
    bucket_manager.update_bucket(bucket)

def ensure_bucket_provisioned(cluster, settings):
    try:
        bucket_manager = cluster.buckets()
        existing_buckets = bucket_manager.get_all_buckets()
        existing_bucket = next((b for b in existing_buckets if b.name == settings.name), None)

        if existing_bucket:
            print(f"Bucket '{settings.name}' already exists.")
            #if bucket_needs_update(existing_bucket, settings):
            #    update_bucket(existing_bucket, settings) 
            #    print(f"Updated '{settings.name}' settings to match required specifications.")
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
    cluster_manager = cluster.buckets()
    bucket_list = cluster_manager.get_all_buckets()
    exists = any(bucket.name == bucket_name for bucket in bucket_list)
    return exists

def initialize_cluster(datastore_conf, cluster_conf, client_conf):
    connection = client_conf['connection']
    credentials = client_conf['credentials']
    specs = cluster_conf['specs']
    url = f"http://{connection['host']}:8091/clusterInit"
    data = {
        'username': credentials['username'],
        'password': credentials['password'],
        'services': ','.join(datastore_conf['services']),
        'hostname': '127.0.0.1',
        'memoryQuota': '256', #specs['ram'],
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
            response = urllib.request.urlopen(request)
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
