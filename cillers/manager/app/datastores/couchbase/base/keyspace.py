from couchbase.cluster import Cluster, Bucket
from couchbase.collection import Collection, Scope
from couchbase.exceptions import (
    CollectionNotFoundException,
    ScopeNotFoundException,
    BucketNotFoundException)
from couchbase.management.collections import CollectionSpec, CollectionManager
from couchbase.management.buckets import BucketSettings, BucketType

class Keyspace:
    cluster: Cluster
    bucket: str
    scope: str | None
    collection: str | None
    settings: dict

    def __init__(
            self,
            cluster: Cluster,
            bucket: str,
            scope: str | None,
            collection: str | None,
            settings: dict | None = None):
        self.cluster = cluster
        self.bucket = bucket
        self.scope = scope
        self.collection = collection
        self.settings = settings or {}
        if collection and not(bucket and scope):
            raise ValueError("If collection is specified, scope and bucket must be specified")

    def query_string(self):
        if self.collection:
            return f"`{self.bucket}`.`{self.scope}`.`{self.collection}`"
        if self.scope:
            return f"`{self.bucket}`.`{self.scope}`"
        return f"`{self.bucket}`"

    def get_bucket(self) -> Bucket:
        return self.cluster.bucket(self.bucket)

    def get_scope(self) -> Scope:
        if not self.scope:
            raise AttributeError("Scope is not specified")
        return self.get_bucket().scope(self.scope)

    def get_collection(self) -> Collection:
        if not self.collection:
            raise AttributeError("Collection is not specified")
        return self.get_scope().collection(self.collection)

    def collection_manager(self) -> CollectionManager:
        return self.get_bucket().collections()

    def exists_collection(self) -> bool:
        try:
            self.get_collection()
        except (CollectionNotFoundException, ScopeNotFoundException, BucketNotFoundException):
            return False
        return True

    def exists_scope(self) -> bool:
        try:
            self.get_scope()
        except (ScopeNotFoundException, BucketNotFoundException):
            return False
        return True

    def exists_bucket(self) -> bool:
        try:
            self.get_bucket()
        except BucketNotFoundException:
            return False
        return True

    def ensure_exists(self):
        if not self.get_bucket():
            self.create_bucket()
        if self.scope:
            if not self.exists_scope():
                self.create_scope()
            if self.collection and not self.exists_collection():
                self.create_collection()

    def create_collection(self):
        if not self.collection:
            raise AttributeError("Collection is not specified")
        collection_spec = CollectionSpec(self.collection, self.scope)
        self.collection_manager().create_collection(collection_spec)

    def create_scope(self):
        if not self.scope:
            raise AttributeError("Scope is not specified")
        self.collection_manager().create_scope(self.scope)

    def create_bucket(self):
        bs = BucketSettings(**{
            **self.settings.get('bucket', {}),
            'name': self.bucket,
            'bucket_type': BucketType.COUCHBASE})
        bucket_manager = self.cluster.buckets()
        bucket_manager.create_bucket(bs)
