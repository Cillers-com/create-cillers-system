from enum import Enum
from typing import Union
from couchbase.diagnostics import ServiceType
from ...helpers import parse_yaml_file, replace_standards
from ...shared_types import EnvironmentId
from .shared import Shared
from .cluster_capella import ClusterCapella
from .cluster_server_single_node import ClusterServerSingleNode

filepaths = { 
    'config': '/root/conf/datastores/couchbase.yml',
    'standards': './standards.yml'
}

class ClusterType(Enum):
    CAPELLA = 'capella'
    SERVER_LOCAL_SINGLE_NODE = 'server_local_single_node'

ClusterUnion = Union[CapellaCluster, LocalServer]

def Clusters:
    clusters: dict[EnvironmentId, dict[str, ClusterUnion]]

    def __init__(self, conf: dict, shared: Shared):
        self.clusters = {}
        for env_id, env_clusters in conf.items():
            clusters[env_id] = {}
            for cluster_id, cluster in env_clusters.items():
                if cluster['type'] == ClusterType.CAPELLA
                    clusters[env_id][cluster_id] = CapellaCluster(cluster, shared)
                elif cluster['type'] == ClusterType.LOCAL_SERVER:
                    clusters[env_id][cluster_id] = LocalServer(cluster, shared)
                else:
                    raise KeyError(f"Unkown cluster type '{cluster['type']}'")

    def get(env_id: EnvironmentId, cluster_id: str):
        return self.clusters[env_id][cluster_id]

class CouchbaseConfig:
    _conf: dict
    shared: Shared
    clusters: Clusters

    def __init__(self, environments):
        conf = parse_yaml_file(filepaths['config'])
        self._conf = conf
        self.shared = Shared(conf['shared'])
        self.clusters = Clusters(conf['clusters'], self.shared)

