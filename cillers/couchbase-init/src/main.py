import os
import sys
from controllers.controller_cluster import ControllerCluster
from controllers.controller_bucket import ControllerBucket
from controllers.controller_data_structure import ControllerDataStructure

def get_env_var(name):
    try:
        return os.environ[name]
    except KeyError:
        raise KeyError(f"Environment variable '{name}' is not set")

COUCHBASE_USERNAME = get_env_var('COUCHBASE_USERNAME')
COUCHBASE_PASSWORD = get_env_var('COUCHBASE_PASSWORD')
COUCHBASE_HOST = get_env_var('COUCHBASE_HOST')
COUCHBASE_TLS = get_env_var('COUCHBASE_TLS').lower() == 'true'
COUCHBASE_MAIN_BUCKET_NAME = get_env_var('COUCHBASE_MAIN_BUCKET_NAME')

data_structure_spec = {"_default": ["items"]}

def main():
    controller_cluster = ControllerCluster(COUCHBASE_HOST, COUCHBASE_USERNAME, COUCHBASE_PASSWORD, COUCHBASE_TLS)
    controller_cluster.ensure_initialized()
    cluster = controller_cluster.connect_with_retry()
    try:
        controller_bucket = ControllerBucket(cluster)
        bucket = controller_bucket.ensure_created(COUCHBASE_MAIN_BUCKET_NAME)
        
        controller_data_structure = ControllerDataStructure(bucket)
        controller_data_structure.create(data_structure_spec)
    finally:
        cluster.close()
    sys.exit(0)

if __name__ == "__main__":
    main()

