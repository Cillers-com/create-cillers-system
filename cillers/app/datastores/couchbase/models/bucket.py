from couchbase.cluster import Cluster
from couchbase.management.buckets import BucketManager, BucketSettings, BucketType
from couchbase.management.collections import CollectionManager
from couchbase.exceptions import CouchbaseException

def ensure_provisioned(cluster: Cluster, settings: BucketSettings):
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

def ensure_scope_exists(cluster: Cluster, bucket_name: str, scope_name: str):
    collection_manager = cluster.bucket(bucket_name).collections()
    scopes = collection_manager.get_all_scopes()
    scope_names = [scope.name for scope in scopes]
    if scope_name not in scope_names:
        collection_manager.create_scope(scope_name)
        print(f"Scope '{scope_name}' created in bucket '{bucket_name}'.")
    else:
        print(f"Scope '{scope_name}' already exists in bucket '{bucket_name}'.")

bucket_type_conf_to_sdk = {
        'couchbase': BucketType.COUCHBASE,
        'memcached': BucketType.MEMCACHED,
        'ephemeral': BucketType.EPHEMERAL
    }

def needs_update(existing_bucket, spec_settings):
    if existing_bucket.get('ram_quota_mb') != spec_settings.get('ramQuotaMB'): return True
    if existing_bucket.numReplicas != spec_settings.numReplicas: return True
    if existing_bucket.durabilityMinLevel != spec_settings.durabilityMinLevel: return True
    return False 

def get_collection(cluster: Cluster, bucket_name: str, scope_name: str, collection_name: str, timeout_seconds: int):
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

def update_bucket(cluster, bucket, settings):
    bucket.settings.ramQuotaMB = settings.ramQuotaMB
    bucket.settings.numReplicas = settings.numReplicas
    bucket.settings.durabilityMinLevel = settings.durabilityMinLevel
    bucket_manager = cluster.buckets()
    bucket_manager.update_bucket(bucket)

#def ensure_exists(bucket_conf):
#    cluster_manager = cluster.buckets()
#    bucket_list = cluster_manager.get_all_buckets()
#    exists = any(bucket.name == bucket_name for bucket in bucket_list)
#    return exists
    
