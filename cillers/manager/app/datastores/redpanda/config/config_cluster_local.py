from .config_cluster import ConfigCluster
from .config_shared import ConfigShared
from .config_cluster_spec_local import ConfigClusterSpecLocal

class ConfigClusterLocal(ConfigCluster):
    _conf: dict
    module: str
    spec: ConfigClusterSpecLocal

    def __init__(self, conf: dict, shared: ConfigShared):
        self._conf = conf
        self.module = conf['module']
        self.spec = ConfigClusterSpecLocal(conf['spec'])
        super().__init__(conf, shared)

