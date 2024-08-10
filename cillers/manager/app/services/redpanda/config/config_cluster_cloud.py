from .config_cluster import ConfigCluster
from .config_shared import ConfigShared
from .config_cluster_spec_cloud import ConfigClusterSpecCapellaUnion, generate_cluster_spec
from .config_cloud import ConfigCloud

class ConfigClusterCloud(ConfigCluster):
    _conf: dict
    cloud: ConfigCloud
    spec: ConfigClusterSpecCapellaUnion

    def __init__(self, conf: dict, shared: ConfigShared):
        self._conf = conf
        self.capella_project_id = conf['capella_project_id']
        self.cloud = ConfigCloud(conf['cloud'])
        self.spec = generate_cluster_spec(conf['spec'])
        super().__init__(conf, shared)

