import os
from . import config_parser
from .config_validators import config_validator

config = config_parser.parse()
config_validator.assert_valid(config)

def get_env_conf():
    return config['environments'][get_env_id()]

def get_env_id():
    return os.getenv("ENVIRONMENT")

def get_datastore_conf(datastore_id):
    conf = config['datastores'][datastore_id]
    if not conf:
        raise KeyError("No matching datastore_conf: {datastore_id}")
    return conf

def get_clients_conf(datastore_id):
    conf = config['clients'][datastore_id]
    if not conf:
        raise KeyError("No matching clients_conf: {datastore_id}")
    return conf

def get_clusters_conf(datastore_id, cluster_ids):
    datastore_conf = get_datastore_conf(datastore_id)
    clusters_conf = datastore_conf['clusters']
    filtered_clusters_conf = {id: conf for id, conf in clusters_conf.items() if id in cluster_ids}
    if len(filtered_clusters_conf) == 0:
        raise KeyError(f"No matching clusters: {datastore_id} [{cluster_ids}]")
    return filtered_clusters_conf

def get_cluster_conf(datastore_type, cluster_id):
    datastore_conf = get_datastore_conf(datastore_type)
    cluster_conf = datastore_conf['clusters'][cluster_id]
    if not cluster_conf:
        raise KeyError(f"No matching cluster: {datastore_type}.{cluster_id}")
    return cluster_conf

def get_metadata_bucket_specs_conf(datastore_type, cluster_id):
    return get_cluster_conf(datastore_type, cluster_id)['metadata_bucket_specs']

def get_client_conf(path: str) -> dict:
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
    return {
        'connection': client['connection'],
        'credentials': credentials
    }

def get_cluster_clients_conf(datastore_id, cluster_id):
    datastore_clients = config['clients'][datastore_id]
    if not datastore_clients:
        raise KeyError(f"No such datastore clients: {datastore_id}")
    cluster_clients = datastore_clients[cluster_id]
    if not cluster_clients:
        raise KeyError(f"No such cluster clients: {datastore_id, cluster_id}")
    return cluster_clients

def get_connection_conf(datastore_type, cluster_id):
    return get_cluster_clients_conf(datastore_type, cluster_id)['connection']

def get_credentials_conf_change(datastore_type, cluster_id):
    cluster_conf = get_cluster_conf(datastore_type, cluster_id)
    cluster_clients = get_cluster_clients_conf(datastore_type, cluster_id)
    change_client_id = cluster_conf['change_client']
    return cluster_clients['credentials'][change_client_id]

def get_metadata_conf(datastore_type):
    return get_datastore_conf(datastore_type)['metadata']

def get_data_structures_conf(datastore_type):
    return get_datastore_conf(datastore_type)['data_structures']

def get_services_conf(datastore_type):
    return get_datastore_conf(datastore_type)['services']
