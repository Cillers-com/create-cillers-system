from couchbase.management.buckets import CreateBucketSettings, BucketType
from app.config import config

class CouchbaseClusterConfig:
    datastore: dict
    clients: dict
    cluster_id: str
    env_id: str

    def __init__(self, cluster_id: str):
        self.cluster_id = cluster_id
        self.datastore = config.get_datastore_conf('couchbase')
        self.clients = config.get_clients_conf('couchbase')[cluster_id]
        self.env_id = config.get_env_id()
        self.metadata = self.datastore['metadata']
        self.cluster = self.datastore['clusters'][self.env_id][self.cluster_id]
        self.metadata_bucket_specs = self.cluster()['metadata_bucket_specs']
        self.data_structures = self.datastore['data_structures']
        self.credentials_change = self.clients['credentials'][self.cluster['change_client_id']]
        self.connection = self.clients['connection']
        self.services = self.datastore['services']
        self.client_params_change = {
            'connection_string': f"{self.connection['protocol']}://{self.connection['host']}",
            'credentials': {
                'type': 'basic',
                'username': self.credentials_change['username'],
                'password': self.credentials_change['password']
            }
        }
        self.cluster_init = {
            'url': f"http://{self.connection['host']}:8091/clusterInit",
            'data': {
                'username': self.credentials_change['username'],
                'password': self.credentials_change['password'],
                'services': ','.join(self.services),
                'hostname': '127.0.0.1',
                'memoryQuota': '256',
                'sendStats': 'false',
                'clusterName': 'cillers',
                'setDefaultMemQuotas': 'true',
                'indexerStorageMode': 'plasma',
                'port': 'SAME'
            }
        }
        self.metadata_bucket_create = CreateBucketSettings(
            name = self.metadata['bucket'],
            bucket_type = BucketType.COUCHBASE,
            ram_quota_mb = self.metadata_bucket_specs['ram'],
            num_replicas = self.metadata_bucket_specs['replicas'],
            durability_min_level = self.metadata_bucket_specs['durability']
        )

    def changes_applied_collection(self, data_structure_id: str):
        return {
            'bucket': self.metadata['bucket'],
            'scope': self.metadata['scope'],
            'collection': f"changes_applied_{data_structure_id}"
        }

    def data_structure_type(self, data_structure_id: str):
        return self.data_structures[data_structure_id]['type']
