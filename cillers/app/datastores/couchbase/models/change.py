from pathlib import Path
import importlib.util
import inspect
from typing import List, Dict, Callable
from couchbase.cluster import Cluster
from couchbase.collection import Collection

def run(cluster: Cluster, data_structures_conf: Dict, metadata_conf: Dict):
    for key, conf in conf.data_structures:
        DataStructure(cluster, key, conf, metadata_conf).change()

class DataStructure:
    directory: DataStructureDirectory
    collection: DataStructureCollection
    type: str
    conf: Dict

    def __init__(self, cluster: Cluster, key: str, conf: Dict, metadata_conf: Dict):
        self.directory = DataStructureDirectory(key)
        self.collection = DataStructureCollection(key, cluster, metadata_conf)
        self.type = conf['type']
        self.conf = conf
        
    def change():
        if (self.type == 'cluster'):
            self.change_cluster()
        elsif (self.type == 'bucket_clones'):
            self.change_bucket_clones()
        elsif (self.type == 'scope_clones'):
            self.change_scope_clones()
        else
            raise Exception(f"Type error '{self.type}'")

    def change_cluster():
        ids = self.to_apply_ids()
        sorted_ids = sorted(ids, key=lambda x: int(x.split('-')[0]))
        for id in sorted_ids:
            change_function = directory.change_function(id)
            change_function(cluster)
            collection.set_applied(id, change_function)

    def change_bucket_clones():
        raise Exception("Not yet implemented")

    def change_scope_clones():
        raise Exception("Not yet implemented")

    def to_apply_ids() -> List[str]:
        all_ids = directory.all_ids()
        applied_ids = collection.applied_ids()
        ids = [id for id in all_ids if id not in applied_ids]

class DataStructureDirectory:
    path: Path
    key: str
    
    def __init__(self, key: str):
        self.key = key
        self.path = Path('/root/change/couchbase') / key

    def all_ids() -> List[str]:
        return [f[:-3]} for f in self.path.rglob('*') if and f.endswith('.py')]

    def change_function(id: str):
        file_path = self.path / f"{id}.py"
        assert file_path.exists()
        spec = importlib.util.spec_from_file_location(id, file_path)
        module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)
        if not hasattr(module, 'change'):
            raise Exception(f"change module 'couchbase.{self.key}.{id}' has no function 'change')
        function = getattr(change_module, 'change')
        if not callable(function):
            raise Exception(f"The 'change' attribute in module 'couchbase.{self.key}.{id}' is not callable")
        return function

class DataStructureCollection:
    key: str
    bucket_name: str
    scope_name: str
    collection_name: str
    cluster: Cluster
    collection: Collection

    def __init__(self, key: str, cluster: Cluster, metadata_conf: Dict):
        self.key = key
        self.bucket_name = metadata_conf['bucket']
        self.scope_name = metadata_conf['scope']
        self.collection_name = f"changes_applied_{key}"
        self.cluster = cluster
        self.collection = cluster.bucket(self.bucket_name).scope(self.scope_name).collection(self.collection_name)

    def applied_ids() -> List[str]: 
        query = f'SELECT META().id FROM `{self.bucket_name}`.`{self.scope_name}`.`{self.collection_name}`'
        result = self.cluster.query(query)
        return [row['id'] for row in result.rows()]

    def set_applied(id: str, change_fn: Callable):
        code = inspect.getsource(change_fn)
        collection.create(id, { change_function: code })

