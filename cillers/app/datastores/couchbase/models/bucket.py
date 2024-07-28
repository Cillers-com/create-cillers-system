from couchbase.cluster import Cluster
from couchbase.management.buckets import BucketSettings, BucketType

def ensure_provisioned(cluster: Cluster, settings: BucketSettings):
    try:
        bucket_manager = cluster.buckets()
        existing_buckets = bucket_manager.get_all_buckets()
        existing_bucket = next((b for b in existing_buckets if b.name == settings.name), None)

        if existing_bucket:
            print(f"Bucket '{settings.name}' already exists.")
        else:
            print(f"Bucket '{settings.name}' does not exist. Creating new bucket...")
            bucket_manager.create_bucket(settings)
            
    except Exception as e:
        print(f"An error occurred: {e}")
        raise

bucket_type_conf_to_sdk = {
        'couchbase': BucketType.COUCHBASE,
        'memcached': BucketType.MEMCACHED,
        'ephemeral': BucketType.EPHEMERAL
    }

