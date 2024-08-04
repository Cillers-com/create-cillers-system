from typing import Union
from ..enums.type_cluster import TypeCluster
from .config_shared import ConfigShared
from .config_cluster_cloud import ConfigClusterCloud
from .config_cluster_local import ConfigClusterLocal

ConfigClusterUnion = Union[ConfigClusterCloud, ConfigClusterLocal]

class_switch = {
    TypeCluster.CAPELLA_MULTI_NODE: ConfigClusterCloud,
    TypeCluster.CAPELLA_SINGLE_NODE: ConfigClusterCloud,
    TypeCluster.LOCAL: ConfigClusterLocal}

class ConfigClusters:
    clusters: dict[str, dict[str, ConfigClusterUnion]]

    def __init__(self, conf: dict, shared: ConfigShared):
        self.clusters = {}
        for env_id, env_clusters in conf.items():
            self.clusters[env_id] = {}
            for c_id, c_conf in env_clusters.items():
                cluster = class_switch[c_conf['type']](c_conf, shared)
                self.clusters[env_id][c_id] = cluster

    def get(self, env_id: str, cluster_id: str) -> ConfigClusterUnion:
        return self.clusters[env_id][cluster_id]

