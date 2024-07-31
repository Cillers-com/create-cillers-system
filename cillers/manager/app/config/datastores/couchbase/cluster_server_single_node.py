from .cluster import Cluster
from .cluster_shared import Shared, BucketSpec
from .connection import Connection

class ClusterServerSingleNodeSpec:
    _conf: dict
    ram: int
    index_ram: int
    fts_ram: int

    def __init__(self, conf: dict):
        self._conf = conf
        self.ram = conf['ram']
        self.index_ram = conf['index_ram']
        self.fts_ram = conf['fts_ram']

class ClusterServerSingleNode(Cluster):
    _conf: dict
    module: str
    spec: ClusterServerSingleNodeSpec

    def __init__(self, conf: dict, shared: Shared):
        self._conf = conf
        self.module = conf['module']
        self.spec = ClusterServerSingleNodeSpec(conf['spec'])
        super.__init__(conf, shared)

