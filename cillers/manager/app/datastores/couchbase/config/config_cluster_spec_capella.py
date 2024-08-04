from typing import Union
from ..enums.node_size import NodeSize
from ..enums.service_tier import ServiceTier
from ..enums.type_cluster import TypeCluster

class ConfigClusterSpecCapellaMultiNode:
    _conf: dict
    size: NodeSize
    service_tier: ServiceTier
    auto_failover: bool
    auto_failover_timeout: int

    def __init__(self, conf: dict):
        self._conf = conf
        self.size = conf['size']
        self.service_tier = conf['service_tier']
        self.auto_failover = conf['auto_failover']
        self.auto_failover_timeout = conf['auto_failover_timeout']

ConfigClusterSpecCapellaUnion = Union[ConfigClusterSpecCapellaMultiNode]

def generate_cluster_spec(conf: dict) -> ConfigClusterSpecCapellaUnion:
    if conf['type'] == TypeCluster.CAPELLA_MULTI_NODE:
        return ConfigClusterSpecCapellaMultiNode(conf)
    raise KeyError("Cluster type not yet implemented '{conf['type']}'.")

