from couchbase.management.buckets import CreateBucketSettings, BucketType
from .shared import Shared
from .cluster_shared import BucketSpec, 
from .credentials import CredentialsBasic, CredentialsType, CredentialsUnion
from .connection import Connection

class Cluster:
    shared: Shared 
    change_credentials_id: str
    metadata_bucket_spec: BucketSpec
    connection: Connection
    credentials: Credentials
    credentials_change: CredentialsUnion
    client_params_change: dict
    cluster_init: dict
    create_bucket_settings_metadata: CreateBucketSettings

    def __init__(self, conf: dict, shared: Shared):
        self.shared = shared
        self.change_credentials_id = conf['change_credentials_id']
        self.metadata_bucket_spec = conf['metadata_bucket_spec']
        self.connection = conf['connection']
        self.credentials = Credentials(conf['credentials'])
        self.credentials_change = self.credentials.get(self.change_credentials_id)
        self.client_params_change = {
            'connection_string': self.connection.connection_string,
            'credentials': self.credentials_change._conf}
        self.cluster_init = {
            'url': f"http://{self.connection.host}:8091/clusterInit",
            'data': {
                'username': self.credentials_change.username,
                'password': self.credentials_change.password,
                'services': ','.join(self.shared.services),
                'hostname': '127.0.0.1',
                'memoryQuota': '256',
                'sendStats': 'false',
                'clusterName': 'cillers',
                'setDefaultMemQuotas': 'true',
                'indexerStorageMode': 'plasma',
                'port': 'SAME'}}
        self.create_bucket_settings_metadata = CreateBucketSettings(
            name = self.shared.metadata.bucket,
            bucket_type = BucketType.COUCHBASE,
            ram_quota_mb = self.metadata_bucket_spec.ram,
            num_replicas = self.metadata_bucket_spec.replicas,
            durability_min_level = self.metadata_bucket_spec.durability)

