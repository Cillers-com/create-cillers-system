import os
import sys
import time
import logging
import rich.traceback

logger = logging.getLogger(__name__)
logging.basicConfig(
    level=logging.INFO, 
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
rich.traceback.install(show_locals=True)

from .config import config
from .datastores.couchbase import manager as couchbase_manager
from .datastores.redpanda import manager as redpanda_manager

module_switch = {
    'couchbase': couchbase_manager,
    'redpanda': redpanda_manager
}

def ensure_cluster_initialized(module, datastore_conf, cluster_conf, client_conf):
    module.ensure_cluster_initialized(datastore_conf, cluster_conf, client_conf)

def ensure_metadata_initialized(module, datastore_conf, cluster_conf, client_conf):
    module.ensure_metadata_initialized(datastore_conf, cluster_conf, client_conf)

def wait_until_ready_for_instructions(module, datastore_conf, cluster_conf, client_conf):
    module.wait_until_ready_for_instructions(client_conf)

def change(module, datastore_conf, cluster_conf, client_conf):
    data_structures_conf = config.get_data_structures_conf(datastore_conf)
    metadata_conf = config.get_metadata_conf(datastore_conf)
    module.change(client_conf, data_structures_conf, metadata_conf)

def exec_on_all_clusters_in_env(env_conf, fn):
    for datastore_type, cluster_ids in env_conf.items():
        clusters_conf = config.get_clusters_conf(datastore_type, cluster_ids)
        for cluster_id in clusters_conf:
            datastore_conf = config.get_datastore_conf(datastore_type)
            cluster_conf = config.get_cluster_conf(datastore_type, cluster_id)
            client_conf = config.get_client(cluster_conf['change_maker_client'])
            module = module_switch[datastore_type]
            fn(module, datastore_conf, cluster_conf, client_conf) 

def change():
    env_conf = config.get_env_conf()
    exec_on_all_clusters_in_env(env_conf, ensure_cluster_initialized)
    exec_on_all_clusters_in_env(env_conf, ensure_metadata_initialized)
    exec_on_all_clusters_in_env(env_conf, wait_until_ready_for_instructions)
    exec_on_all_clusters_in_env(env_conf, change)
#    while True: time.sleep(10)
    sys.exit(0)

def validate_config():
    # Config is validated when the config module is imported
    sys.exit(0)

