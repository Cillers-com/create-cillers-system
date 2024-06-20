import os
import sys
import logging
import rich.traceback
from . import config, couchbase

logger = logging.getLogger(__name__)

def ensure_cluster_initialized(data_store_type, cluster_config, client_config):
    if data_store_type == 'couchbase':
        print(f"COUCHBASE Config: {cluster_config}, client: {client_config}")
    
        couchbase.wait_until_ready(client_config)
    elif data_store_type == 'redpanda':
        print(f"REDPANDA Config: {cluster_config}")
        #redpanda.wait_until_ready(cluster_config)

def change():
    for data_store_id, clusters in config.get_data_stores_to_change().items():
        data_store_config = config.get_data_store(data_store_id)
        data_store_type = data_store_config['type']
        for cluster_id in clusters:
            cluster_config = config.get_cluster(data_store_id, cluster_id)
            client_config = config.get_client(cluster_config['change_maker_client'])
            ensure_cluster_initialized(data_store_type, cluster_config, client_config)

def main():
    logging.basicConfig(
        level=logging.INFO, 
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    )
    rich.traceback.install(show_locals=True)
    change()
    sys.exit(0)

