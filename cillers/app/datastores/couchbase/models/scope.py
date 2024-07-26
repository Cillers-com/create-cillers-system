from couchbase.cluster import Cluster
from couchbase.management.collections import ScopeSpec, ScopeNotFoundException

def ensure_exists(cluster: Cluster, bucket_name: str, scope_name: str):
    if not exists(cluster, bucket_name, scope_name):
        create(cluster, bucket_name, scope_name)

def exists(cluster: Cluster, bucket_name: str, scope_name: str) -> Boolean:
    try:
        cluster.bucket(bucket_name).scope(scope_name)
    except ScopeNotFoundException:
        return False
    return True 

def create(cluster: Cluster, bucket_name: str, scope_name: str):
    bucket = cluster.bucket(bucket_name)
    collection_manager = bucket.collections()
    collection_manager.create_scope(scope_name)

