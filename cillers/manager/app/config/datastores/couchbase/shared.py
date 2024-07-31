from typing import Union, Protocol

class Metadata:
    _conf: dict
    bucket: str
    scope: str

    def __init__(self, conf: dict):
        self._conf = conf
        self.bucket = conf['bucket']
        self.scope = conf['scope']

class DataStructureType(Enum):
    CLUSTER = 'cluster'
    BUCKET_CLONES = 'bucket_clones'
    SCOPE_CLONES = 'scope_clones'

class DataStructureCluster(TypeProtocol):
    _conf: dict
    bucket_prefixes_to_exclude: list(str)
    scope_prefixes_to_exclude: list(str)

    def __init__(self, conf: dict):
        self._conf = conf
        self.bucket_prefixes_to_exclude = conf.get('bucket_prefixes_to_exclude', [])
        self.scope_prefixes_to_exclude = conf.get('scope_prefixes_to_exclude', [])

class DataStructureBucketClones(TypeProtocol):
    _conf: dict
    prefix: str

    def __init__(self, conf: dict):
        self._conf = conf
        self.prefix = conf['prefix']

class DataStructureScopeClones(TypeProtocol):
    _conf: dict
    type: str
    bucket: str
    prefix: str

    def __init(self, conf: dict):
        self._conf = conf
        self.bucket = conf['bucket']
        self.prefix = conf['prefix']

DataStructureUnion = Union[
        DataStructureCluster, 
        DataStructureBucketClones, 
        DataStructureScopeClones]

class Shared:
    _conf: dict
    metadata: Metadata
    data_structures: dict[str, DataStructureUnion]
    capella_projects: dict[str, CapellaProject]
    services: list[ServiceType]

    def __init__(self, conf: dict):
        self._conf = conf
        self.metadata = Metadata(conf['metadata'])
        self.data_structures = {ds_id: DataStructure(ds) for ds_id, ds in conf['data_structures'].items()} 
        self.capella_projects = (cp_id: CapellaProject(cp) for cp_id, cp in conf['capella_projects'].items()} 
        self.services = conf['services']

    def changes_applied_collection(self, data_structure_id: str):
        return {
                'bucket': self.metadata.bucket,
                'scope': self.metadata.scope,
                'collection': f"changes_applied_{data_structure_id}"
            }

    def data_structure(self, data_structure_id: str) -> DataStructureUnion:
        data_structure = self.data_structures.get(data_structure_id)
        assert data_structure
        return data_structure

