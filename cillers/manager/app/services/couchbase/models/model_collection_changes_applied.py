import inspect
from typing import Callable
from couchbase.cluster import Cluster
from ..base.keyspace import Keyspace

class ModelCollectionChangesApplied():
    cluster: Cluster
    keyspace: Keyspace

    def __init__(self, cluster: Cluster, keyspace: Keyspace):
        self.cluster = cluster
        self.keyspace = keyspace
        
    def ensure_exists(self):
        self.keyspace.ensure_exists()

    def applied_ids(self) -> list[str]:
        query = f'SELECT META().id FROM {self.keyspace.query_string()}'
        result = self.cluster.query(query)
        return [row['id'] for row in result.rows()]

    def set_applied(self, change_id: str, change_fn: Callable):
        code = inspect.getsource(change_fn)
        self.keyspace.get_collection().create(change_id, { 'change_function': code })

