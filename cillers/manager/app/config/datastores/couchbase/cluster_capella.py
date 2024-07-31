from .cluster import Cluster

class CapellaProject:
    _conf: dict
    organization_id: str
    project_id: str

    def __init__(self, conf: dict):
        self._conf = conf
        self.organization_id = conf['organization_id']
        self.project_id = conf['project_id']

class CloudProviderCapella(Enum):
    AWS = 'aws'
    GCP = 'gcp'
    AZURE = 'azure'

class CloudCapella:
    _conf: dict
    provider: CloudProviderCapella
    region: str

    def __init__(self, conf: dict):
        self._conf = conf
        self.provider = conf['provider']
        self.region = conf['region']

class NodeSize(Enum):
    SMALL: 'small'

class ServiceTier(Enum):
    DEVELOPER_PRO: 'developer_pro'

class ClusterSpecCapellaMultiNode:
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

class CloudCapella:
    _conf: dict
    provider: str
    region: str

    def __init__(self, conf: dict):
        self_conf = 
        self.provider = conf['provider']
        self.region = conf['region']

class ClusterCapella(Cluster):
    _conf: dict
    capella_project_id: str
    cloud: CloudCapella
    spec: ClusterCapellaSpec
    service_groups: dict[str, CapellaServiceGroup]

    def __init__(self, conf: dict, shared: Shared):
        self._conf = conf
        self.capella_project_id = conf['capella_project_id']
        self.cloud = CloudCapella(conf['cloud'])
        self.spec = ClusterCapellaSpec(conf['spec'])
        self.service_groups = conf['service_groups']
        super.__init__(conf, shared)

