from typing import Union
from ..enums.type_data_structure import TypeDataStructure

class ConfigDataStructureCluster:
    _conf: dict
    bucket_prefixes_to_exclude: list[str]
    scope_prefixes_to_exclude: list[str]

    def __init__(self, conf: dict):
        self._conf = conf
        self.type = TypeDataStructure.CLUSTER
        self.bucket_prefixes_to_exclude = conf.get('bucket_prefixes_to_exclude', [])
        self.scope_prefixes_to_exclude = conf.get('scope_prefixes_to_exclude', [])

class ConfigDataStructureBucketClones:
    _conf: dict
    prefix: str

    def __init__(self, conf: dict):
        self._conf = conf
        self.type = TypeDataStructure.BUCKET_CLONES
        self.prefix = conf['prefix']

class ConfigDataStructureScopeClones:
    _conf: dict
    bucket: str
    prefix: str

    def __init__(self, conf: dict):
        self._conf = conf
        self.type = TypeDataStructure.SCOPE_CLONES
        self.bucket = conf['bucket']
        self.prefix = conf['prefix']

ConfigDataStructureUnion = Union[
        ConfigDataStructureCluster, 
        ConfigDataStructureBucketClones, 
        ConfigDataStructureScopeClones]

class_switch = {
    TypeDataStructure.CLUSTER: ConfigDataStructureCluster,
    TypeDataStructure.BUCKET_CLONES: ConfigDataStructureBucketClones,
    TypeDataStructure.SCOPE_CLONES: ConfigDataStructureScopeClones}

def generate_data_structures(conf: dict) -> dict[str, ConfigDataStructureUnion]:
    data_structures = {}
    for ds_id, ds_conf in conf['data_structures'].items():
        data_structures[ds_id] = class_switch[ds_id](ds_conf)
    return data_structures

