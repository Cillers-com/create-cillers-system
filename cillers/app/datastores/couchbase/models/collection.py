from couchbase.cluster import Cluster
from couchbase.collection import CollectionSpec, CollectionNotFoundException

def exists(cluster: Cluster, bucket_name: str, scope_name: str, collection_name: str):
    try:
        cluster.bucket(bucket_name).scope(scope_name).collection(collection_name)
    except (CollectionNotFoundException):
        return false
    return true

def create(cluster: Cluster, bucket_name: str, scope_name: str, collection_name: str):
    collection_spec = CollectionSpec(collection_name, scope_name)
    collection_manager = bucket.collections()
    collection_manager.create_collection(collection_spec)

