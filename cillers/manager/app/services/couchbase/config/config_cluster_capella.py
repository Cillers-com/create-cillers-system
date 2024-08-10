from .config_cluster import ConfigCluster
from .config_shared import ConfigShared
from .config_service_group import ConfigServiceGroup, generate_service_groups
from .config_cluster_spec_capella import ConfigClusterSpecCapellaUnion, generate_cluster_spec
from .config_cloud_capella import ConfigCloudCapella

class ConfigClusterCapella(ConfigCluster):
    _conf: dict
    capella_project_id: str
    cloud: ConfigCloudCapella
    spec: ConfigClusterSpecCapellaUnion
    service_groups: dict[str, ConfigServiceGroup]

    def __init__(self, conf: dict, shared: ConfigShared):
        self._conf = conf
        self.capella_project_id = conf['capella_project_id']
        self.cloud = ConfigCloudCapella(conf['cloud'])
        self.spec = generate_cluster_spec(conf['spec'])
        self.service_groups = generate_service_groups(conf['service_groups']) 
        super().__init__(conf, shared)

