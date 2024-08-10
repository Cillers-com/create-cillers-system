from config import config
from typing import List, Dict

class RedpandaClusterConfig:
    cluster_id: str
    datastore: Dict
    clients: Dict
    env_id: str
    metadata: Dict
    cluster: Dict
    metadata_topics_specs: Dict
    data_structures: Dict
    connection: Dict
    client_params_change: Dict
    
    def __init__(self, cluster_id: str):
        self.cluster_id = cluster_id
        self.datastore = config.get_datastore_conf('couchbase')
        self.clients = config.get_clients_conf('couchbase')[cluster_id]
        self.env_id = config.get_env_id()
        self.metadata = self.datastore['metadata']
        self.cluster = self.datastore['clusters'][self.env_id][self.cluster_id]
        self.metadata_topics_specs = self.cluster()['metadata_topics_specs']
        self.data_structures = self.datastore['data_structures']
        self.connection = self.clients['connection']
        self.connection['bootstrap_servers'] = [f"{s['host']}:{s['port']}" for s in self.connection['bootstrap_servers']]
        self.client_params_change = {
            'client_id': 'change',
            'bootstrap_servers': self.connection['bootstrap_servers']
        }
        credentials_change = self.clients['credentials'][self.cluster['change_client_id']]
        if credentials_change:
            self.client_params_change.update(credentials_change)
        
    def changes_applied_topic(data_structure_id: str):
        return f"cillers_metadata_changes_applied_{data_structure_id}",

    def data_structure_type(data_structure_id: str):
        return self.data_structures[data_structure_id]['type']

