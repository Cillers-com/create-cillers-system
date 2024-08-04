from couchbase.management.buckets import BucketSettings
from ...shared.config.config_credentials import ConfigCredentials
from .config_shared import ConfigShared
from .config_connection import ConfigConnection

class ConfigCluster:
    shared: ConfigShared
    credentials_id_change: str
    bucket_settings_metadata: BucketSettings
    connection: ConfigConnection
    credentials: ConfigCredentials

    def __init__(self, conf: dict, shared: ConfigShared):
        self.shared = shared
        self.credentials_id_change = conf['credentials_id_change']
        self.bucket_settings_metadata = BucketSettings(**conf['bucket_spec_metadata'])
        self.connection = ConfigConnection(conf['connection'])
        self.credentials = ConfigCredentials(conf['credentials'])
