from pathlib import Path
import importlib.util
import inspect
from typing import List, Dict, Callable
from couchbase.cluster import Cluster
from couchbase.collection import Collection
from ..cluster_config import CouchbaseClusterConfig

class DataStructureDirectory:
    path: Path
    data_structure_id: str
    
    def __init__(self, data_structure_id: str):
        self.data_structure_id = data_structure_id 
        self.path = Path('/root/change/couchbase') / data_structure_id

    def all_ids(self) -> List[str]:
        return [f.stem for f in self.path.rglob('*.py')]

    def change_function(self, change_id: str) -> Callable:
        filename = f"{change_id}.py"
        filepath = self.path / filename
        assert filepath.exists()
        spec = importlib.util.spec_from_file_location(filename, filepath)
        module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)
        if not hasattr(module, 'change'):
            raise Exception(f"change module 'couchbase.{self.data_structure_id}.{change_id}' has no function 'change'")
        function = getattr(module, 'change')
        if not callable(function):
            raise Exception(f"The 'change' attribute in module 'couchbase.{self.data_structure_id}.{change_id}' is not callable")
        return function

class DataStructureCollection:
    data_structure_id: str
    bucket_name: str
    scope_name: str
    collection_name: str
    cluster: Cluster
    collection: Collection

    def __init__(self, data_structure_id: str, cluster: Cluster, metadata_conf: Dict):
        self.data_structure_id = data_structure_id
        self.bucket_name = metadata_conf['bucket']
        self.scope_name = metadata_conf['scope']
        self.collection_name = f"changes_applied_{data_structure_id}"
        self.cluster = cluster
        self.collection = cluster.bucket(self.bucket_name).scope(self.scope_name).collection(self.collection_name)

    def applied_ids(self) -> List[str]: 
        query = f'SELECT META().id FROM `{self.bucket_name}`.`{self.scope_name}`.`{self.collection_name}`'
        result = self.cluster.query(query)
        return [row['id'] for row in result.rows()]

    def set_applied(self, change_id: str, change_fn: Callable):
        code = inspect.getsource(change_fn)
        self.collection.create(change_id, { 'change_function': code })

class DataStructure:
    cluster: Cluster
    directory: DataStructureDirectory
    collection: DataStructureCollection
    type: str
    conf: CouchbaseClusterConfig
    env_id: str

    def __init__(self, cluster: Cluster, data_structure_id: str, conf: CouchbaseClusterConfig):
        self.directory = DataStructureDirectory(data_structure_id)
        self.collection = DataStructureCollection(data_structure_id, cluster, conf.metadata)
        self.type = conf.data_structure_type(data_structure_id)
        self.conf = conf
        self.env_id = conf.env_id
        
    def change(self):
        if (self.type == 'cluster'):
            self.change_cluster()
        elif (self.type == 'bucket_clones'):
            self.change_bucket_clones()
        elif (self.type == 'scope_clones'):
            self.change_scope_clones()
        else:
            raise Exception(f"Type error '{self.type}'")

    def change_cluster(self):
        ids = self.to_apply_ids()
        sorted_ids = sorted(ids, key=lambda x: int(x.split('-')[0]))
        for change_id in sorted_ids:
            change_function = self.directory.change_function(change_id)
            num_params = len(inspect.signature(change_function).parameters)
            if num_params == 1:
                change_function(self.cluster)
            elif num_params == 2:
                change_function(self.cluster, self.env_id)
            else:
                raise Exception("Change functions must take 1 or 2 parameters")
            self.collection.set_applied(id, change_function)

    def change_bucket_clones(self):
        raise Exception("Not yet implemented")

    def change_scope_clones(self):
        raise Exception("Not yet implemented")

    def to_apply_ids(self) -> List[str]:
        all_ids = self.directory.all_ids()
        applied_ids = self.collection.applied_ids()
        return [id for id in all_ids if id not in applied_ids]

def run(cluster: Cluster, conf: CouchbaseClusterConfig):
    for data_structure_id in conf.data_structures:
        DataStructure(cluster, data_structure_id, conf).change()
