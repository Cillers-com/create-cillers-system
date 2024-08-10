from couchbase.cluster import Cluster
from couchbase.management.buckets import BucketSettings
from ..base.keyspace import Keyspace
from ..config.config_metadata import ConfigMetadata

class ModelMetadata:
    cluster: Cluster
    conf_metadata: ConfigMetadata
    bucket_settings: BucketSettings

    def __init__(
            self,
            cluster: Cluster,
            conf_metadata: ConfigMetadata,
            bucket_settings: BucketSettings):
        self.cluster = cluster
        self.conf_metadata = conf_metadata
        self.bucket_settings = bucket_settings

    def ensure_initialized(self):
        self.generate_keyspace().ensure_exists()

    def generate_keyspace(self) -> Keyspace:
        return Keyspace(
            self.cluster,
            self.conf_metadata.bucket,
            self.conf_metadata.scope,
            None,
            { 'bucket': self.bucket_settings })

    def generate_keyspace_with_collection(self, collection: str):
        keyspace = self.generate_keyspace()
        keyspace.collection = collection
        return keyspace
