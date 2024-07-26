from pathlib import Path
import importlib.util
import inspect
from typing import List, Dict, Callable
from couchbase.cluster import Cluster
from couchbase.collection import Collection

class DataStructureDirectory:
    path: Path
    key: str
    
    def __init__(self, key: str):
        self.key = key
        self.path = Path('/root/change/couchbase') / key

    def all_ids() -> List[str]:
        return [f.stem for f in self.path.rglob('*.py')]

    def change_function(id: str) -> Callable:
        filename = f"{id}.py"
        filepath = self.path / filename 
        assert filepath.exists()
        spec = importlib.util.spec_from_file_location(filename, filepath)
        module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)
        if not hasattr(module, 'change'):
            raise Exception(f"change module 'couchbase.{self.key}.{id}' has no function 'change')
        function = getattr(module, 'change')
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

class DataStructure:
    directory: DataStructureDirectory
    collection: DataStructureCollection
    type: str
    conf: Dict
    env_id: str

    def __init__(self, cluster: Cluster, key: str, conf: Dict, metadata_conf: Dict, env_id: str):
        self.directory = DataStructureDirectory(key)
        self.collection = DataStructureCollection(key, cluster, metadata_conf)
        self.type = conf['type']
        self.conf = conf
        self.env_id = env_id
        
    def change():
        if (self.type == 'cluster'):
            self.change_cluster(env_id)
        elsif (self.type == 'bucket_clones'):
            self.change_bucket_clones(env_id)
        elsif (self.type == 'scope_clones'):
            self.change_scope_clones(env_id)
        else
            raise Exception(f"Type error '{self.type}'")

    def change_cluster():
        ids = self.to_apply_ids()
        sorted_ids = sorted(ids, key=lambda x: int(x.split('-')[0]))
        for id in sorted_ids:
            change_function = directory.change_function(id)
            num_params = len(inspect.signature(function).parameters)
            if num_params == 1:
                change_function(cluster)
            elsif num_params == 2:
                change_function(cluster, self.env_id)
            collection.set_applied(id, change_function)

    def change_bucket_clones():
        raise Exception("Not yet implemented")

    def change_scope_clones():
        raise Exception("Not yet implemented")

    def to_apply_ids() -> List[str]:
        all_ids = directory.all_ids()
        applied_ids = collection.applied_ids()
        return [id for id in all_ids if id not in applied_ids]

def run(cluster: Cluster, data_structures_conf: Dict, metadata_conf: Dict):
    for key, conf in data_structures_conf:
        DataStructure(cluster, key, conf, metadata_conf).change()

