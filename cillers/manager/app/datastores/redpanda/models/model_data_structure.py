import inspect
from couchbase.cluster import Cluster
from ....base.environment import env_id
from ..config.config_data_structures import (
    ConfigDataStructureUnion,
    ConfigDataStructureCluster,
    ConfigDataStructureBucketClones,
    ConfigDataStructureScopeClones)
from .model_directory_changes import ModelDirectoryChanges
from .model_collection_changes_applied import ModelCollectionChangesApplied
from .model_metadata import ModelMetadata

class ModelDataStructure:
    cluster: Cluster
    directory_changes: ModelDirectoryChanges
    collection_changes_applied: ModelCollectionChangesApplied
    conf: ConfigDataStructureUnion

    def __init__(
            self,
            cluster: Cluster,
            data_structure_id: str,
            conf: ConfigDataStructureUnion,
            metadata: ModelMetadata):
        self.cluster = cluster
        self.conf = conf
        self.directory = ModelDirectoryChanges(data_structure_id)
        self.metadta = metadata
        k = metadata.generate_keyspace_with_collection(f'changes_applied_{data_structure_id}')
        self.collection_changes_applied = ModelCollectionChangesApplied(cluster, k)
        self.directory.ensure_exists()
        self.collection_changes_applied.ensure_exists()

    def change(self):
        if isinstance(self.conf, ConfigDataStructureCluster):
            self.change_cluster()
        elif isinstance(self.conf, ConfigDataStructureBucketClones):
            self.change_bucket_clones()
        elif isinstance(self.conf, ConfigDataStructureScopeClones):
            self.change_scope_clones()
        else:
            raise AttributeError(f"Unknown type of config '{self.conf}'")

    def change_cluster(self):
        ids = self.to_apply_ids()
        sorted_ids = sorted(ids, key=lambda x: int(x.split('-')[0]))
        for change_id in sorted_ids:
            self.call_change_function(change_id)

    def change_bucket_clones(self):
        raise NotImplementedError

    def change_scope_clones(self):
        raise NotImplementedError

    def call_change_function(self, change_id: str):
        fn = self.directory.change_function(change_id)
        num_params = len(inspect.signature(fn).parameters)
        if num_params == 1:
            fn(self.cluster)
        elif num_params == 2:
            fn(self.cluster, env_id)
        else:
            raise Exception("Change functions must take 1 or 2 parameters")
        self.collection_changes_applied.set_applied(id, fn)

    def to_apply_ids(self) -> list[str]:
        all_ids = self.directory.all_ids()
        applied_ids = self.collection_changes_applied.applied_ids()
        return [id for id in all_ids if id not in applied_ids]

