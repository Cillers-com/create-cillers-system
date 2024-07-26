from couchbase.cluster import Cluster

def change(cluster: Cluster):
    bucket = cluster.bucket('main')
    collection_manager = bucket.collections()
    collection_spec = CollectionSpec('items', '_default')
    collection_manager.create_collection(collection_spec)
        
