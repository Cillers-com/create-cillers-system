import os
import copy
from . import config_parser
from .config_validators import config_validator 

config = config_parser.parse()
config_validator.assert_valid(config)

def get_env_conf():
    env = os.getenv("ENVIRONMENT")  
    env_conf = config['environments'][env]
    return copy.deepcopy(env_conf)

def get_datastore_conf(type):
    datastore_conf = config['datastores'][type]
    return copy.deepcopy(datastore_conf) 

def get_clusters_conf(datastore_type, cluster_ids):
    datastore_conf = get_datastore_conf(datastore_type)
    all_clusters_conf = datastore_conf['clusters']
    filtered_clusters_conf = {id: conf for id, conf in all_clusters_conf.items() if id in cluster_ids}
    return copy.deepcopy(filtered_clusters_conf)

def get_cluster_conf(datastore_type, cluster_id):
    datastore_conf = get_datastore_conf(datastore_type)
    cluster_conf = datastore_conf['clusters'][cluster_id]
    return copy.deepcopy(cluster_conf)

def get_client(path):
    parts = path.split('.')
    assert len(parts) == 3
    service_module, service_instance, credentials_id = parts
    client = config['clients'][service_module][service_instance]
    return {
        'connection': copy.deepcopy(client['connection']),
        'credentials': copy.deepcopy(client['credentials'][credentials_id])
    }

def get_data_structures_conf(datastore_conf):
    return datastore_conf['data_structures']

def get_metadata_conf(datastore_conf):
    return datastore_conf['metadata']

