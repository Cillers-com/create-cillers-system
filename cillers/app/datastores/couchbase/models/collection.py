from dataclasses import dataclass
from couchbase.cluster import Cluster
from couchbase.management.collections import CollectionSpec
from couchbase.exceptions import CollectionNotFoundException

@dataclass
class Keyspace:
    bucket: str
    scope: str
    collection: str

def ensure_exists(cluster: Cluster, keyspace: Keyspace):
    if not exists(cluster, keyspace):
        create(cluster, keyspace)

def exists(cluster: Cluster, keyspace: Keyspace) -> bool:
    try:
        cluster.bucket(keyspace.bucket).scope(keyspace.scope).collection(keyspace.collection)
    except CollectionNotFoundException:
        return False
    return True

def create(cluster: Cluster, keyspace: Keyspace):
    collection_spec = CollectionSpec(keyspace.collection, keyspace.scope)
    bucket = cluster.bucket(keyspace.bucket)
    collection_manager = bucket.collections()
    collection_manager.create_collection(collection_spec)
