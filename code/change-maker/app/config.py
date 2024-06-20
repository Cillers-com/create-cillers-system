import os
import copy
from . import config_parser, config_validator

config = config_parser.parse()
config_validator.assert_valid(config)

def get_data_stores_to_change():
    environment = os.getenv("ENVIRONMENT")  
    data_stores = config['change_maker'][environment]
    return copy.deepcopy(data_stores)

def get_data_store(id):
    data_store = config['data_stores'][id]
    return copy.deepcopy(data_store) 

def get_cluster(data_store_id, cluster_id):
    cluster = get_data_store(data_store_id)['clusters'][cluster_id]
    return copy.deepcopy(cluster)

def get_client(change_maker_client_path):
    parts = change_maker_client_path.split('.')
    assert len(parts) == 3
    service_module, service_instance, credentials_id = parts
    client = config['clients'][service_module][service_instance]
    return {
        'connection': copy.deepcopy(client['connection']),
        'credentials': copy.deepcopy(client['credentials'][credentials_id])
    }

