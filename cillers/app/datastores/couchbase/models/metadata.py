from pathlib import Path
from couchbase.cluster import Cluster
from couchbase.bucket import BucketSettings
from config import config
from . import bucket, collection 

def ensure_initialized(cluster: Cluster, conf: config.ClusterChangeConfig):
    bucket_settings = generate_metadata_bucket_settings(conf)
    cluster = get_cluster(conf)
    bucket.ensure_provisioned(cluster, bucket_settings)
    bucket.ensure_scope_exists(cluster, bucket_settings.name, 'cillers_metadata')
    ensure_change_constructs_initialized(cluster, conf)

def generate_metadata_bucket_settings(conf: config.ClusterChangeConfig) -> BucketSettings:
    bucket_settings = BucketSettings(
        name = conf.metadata['bucket'],
        bucket_type = BucketType.COUCHBASE,
        ram_quota_mb = conf.metadata_bucket_specs['ram'],
        num_replicas = conf.metadata_bucket_specs['replicas'],
        durability_min_level = conf.metadata_bucket_specs['durability']
    )
    return bucket_settings

def ensure_change_constructs_initialized(cluster: Cluster, conf: config.ClusterChangeConfig):
    for key, _ in conf.data_structures:
        ensure_change_directory_exists(key)
        ensure_change_collection_exists(cluster, key)

def ensure_change_directory_exists(key: str): 
    change_file_dir = Path('/root/change/couchbase') / key
    change_file_dir.mkdir(parents=True, exist_ok=True)

def ensure_change_collection_exists(cluster: Cluster, conf: config.ClusterChangeConfig, key: str):
    bucket_name = config.metadata['bucket']
    scope_name = config.metadata['scope']
    collection_name = f"changes_applied_{key}"
    if not collection.exists(cluster, bucket_name, scope_name, collection_name):
        collection.create(cluster, bucket_name, scope_name, collection_name)

