import os
import sys
import time
import logging
import rich.traceback
from typing import Dict
from .config import config
from .datastores.couchbase import controller as couchbase_controller
from .datastores.redpanda import controller as redpanda_controller

logger = logging.getLogger(__name__)
logging.basicConfig(
    level=logging.INFO, 
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)

rich.traceback.install(show_locals=True)

datastore_controller_switch = {
    'couchbase': couchbase_controller,
    'redpanda': redpanda_controller
}

def get_datastore_controller(datastore_type):
    datastore_controller = datastore_controller_switch[datastore_type]
    if not datastore_controller:
        raise KeyError(f"No such datastore controller: {datastore_type}")
    return datastore_controller

def change_cluster(datastore_type: str, cluster_id: str):
    conf = config.ClusterChangeConfig(datastore_type, cluster_id)
    controller = get_datastore_controller(datastore_type)
    controller.change_cluster(conf)

def change():
    env_conf = config.get_env_conf()
    for datastore_type, cluster_ids in env_conf.items():
        clusters_conf = config.get_clusters_conf(datastore_type, cluster_ids)
        for cluster_id in clusters_conf:
            change_cluster(datastore_type, cluster_id)
    sys.exit(0)

def validate_config():
    # Config is validated when the config module is imported
    sys.exit(0)

