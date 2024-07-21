import os
import copy
from . import config_parser
from .config_validators import config_validator 
from typing import Dict, List

config = config_parser.parse()
config_validator.assert_valid(config)

class ClientConfig:
    connection: Dict
    credentials: Dict

    def __init__(self, conf: Dict):
        self.connection = conf['connection']
        self.credentials = conf['credentials']

class ClusterChangeConfig:
    datastore_type: str
    cluster_id: str
    cluster: Dict
    connection: Dict
    credentials: Dict
    metadata: Dict
    data_structures: Dict
    services: List

    def __init__(self, datastore_type: str, cluster_id: str):
        self.datastore_type = datastore_type
        self.metadata = get_metadata_conf(datastore_type)
        self.metadata_bucket_specs = get_metadata_bucket_specs_conf(datastore_type)
        self.data_structures = get_data_structures_conf(datastore_type)
        self.cluster_id = cluster_id
        self.cluster = get_cluster_conf(datastore_type, cluster_id),
        self.connection = get_connection_conf(datastore_type, cluster_id)
        self.credentials = get_change_credentials_conf(datastore_type, cluster_id)
        self.services = get_services_conf(datastore_type)

def get_env_conf():
    env = os.getenv("ENVIRONMENT")  
    env_conf = config['environments'][env]
    return env_conf

def get_datastore_conf(type):
    datastore_conf = config['datastores'][type]
    if not datastore_conf:
        raise KeyError("No matching datastore_conf: {type}")
    return datastore_conf 

def get_clusters_conf(datastore_type, cluster_ids):
    datastore_conf = get_datastore_conf(datastore_type)
    all_clusters_conf = datastore_conf['clusters']
    filtered_clusters_conf = {id: conf for id, conf in all_clusters_conf.items() if id in cluster_ids}
    if len(filtered_clusters_conf) == 0:
        raise KeyError(f"No matching clusters: {datastore_type} [{cluster_ids}]")
    return filtered_clusters_conf

def get_cluster_conf(datastore_type, cluster_id):
    datastore_conf = get_datastore_conf(datastore_type)
    cluster_conf = datastore_conf['clusters'][cluster_id]
    if not cluster_conf:
        raise KeyError(f"No matching cluster: {datastore_type}.{cluster_id}")
    return cluster_conf

def get_metadata_bucket_specs_conf(datastore_type, cluster_id):
    return get_cluster_conf(datastore_type, cluster_id)['metadata_bucket_specs']

def get_client_conf(path: str) -> ClientConfig:
    parts = path.split('.')
    assert len(parts) == 3
    service_module, service_instance, credentials_id = parts
    service_module = config['clients'][service_module]
    if not service_module:
        raise KeyError(f"No matching service module: {service_module}")
    client = service_module[service_instance]
    if not client:
        raise KeyError(f"No matching client: {service_module}.{service_instance}")
    credentials = client['credentials'][credentials_id]
    if not credentials:
        raise KeyError(f"No matching credentials: {path}")
    return ClientConfig(
        connection=client['connection'],
        credentials=credentials
    )

def get_cluster_clients_conf(datastore_type, cluster_id):
    cluster_conf = get_cluster_conf(datastore_type, cluster_id) 
    datastore_clients = config['clients'][datastore_type]
    if not datastore_clients:
        raise KeyError(f"No such datastore clients: {datastore_type}")
    cluster_clients = datastore_clients[cluster_id]
    if not cluster_clients:
        raise KeyError(f"No such cluster clients: {datastore_type, cluster_id}")
    return cluster_clients

def get_connection_conf(datastore_type, cluster_id):
    return get_cluster_clients_conf(datastore_type, cluster_id)['connection']

def get_change_credentials_conf(datastore_type, cluster_id):
    cluster_conf = get_cluster_conf(datastore_type, cluster_id)
    cluster_clients = get_cluster_clients_conf(datastore_type, cluster_id)
    change_client = cluster_conf['change_client']

def get_metadata_conf(datastore_type):
    return get_datastore_conf(datastore_type)['metadata']

def get_data_structures_conf(datastore_type):
    return get_datastore_conf(datastore_type)['data_structures']

def get_services_conf(datastore_type):
    return get_datastore_conf(datastore_type)['services']
