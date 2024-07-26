from couchbase.cluster import Cluster
from couchbase.management.collections import CollectionSpec, CollectionNotFoundException

def ensure_exists(cluster: Cluster, bucket_name: str, scope_name: str, collection_name: str):
    if not exists(cluster, bucket_name, scope_name, collection_name):
        create(cluster, bucket_name, scope_name, collection_name)

def exists(cluster: Cluster, bucket_name: str, scope_name: str, collection_name: str) -> Boolean:
    try:
        cluster.bucket(bucket_name).scope(scope_name).collection(collection_name)
    except (CollectionNotFoundException):
        return False
    return True

def create(cluster: Cluster, bucket_name: str, scope_name: str, collection_name: str):
    collection_spec = CollectionSpec(collection_name, scope_name)
    bucket = cluster.bucket(bucket_name)
    collection_manager = bucket.collections()
    collection_manager.create_collection(collection_spec)

