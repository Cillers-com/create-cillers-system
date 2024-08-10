from couchbase.diagnostics import ServiceType
from .config_data_structures import ConfigDataStructureUnion, generate_data_structures
from .config_capella_project import ConfigCapellaProject, generate_capella_projects
from .config_metadata import ConfigMetadata

class ConfigShared:
    _conf: dict
    metadata: ConfigMetadata
    data_structures: dict[str, ConfigDataStructureUnion]
    capella_projects: dict[str, ConfigCapellaProject]
    services: list[ServiceType]

    def __init__(self, conf: dict):
        self._conf = conf
        self.metadata = ConfigMetadata(conf['metadata'])
        self.data_structures = generate_data_structures(conf['data_structures'])
        self.capella_projects = generate_capella_projects(conf['capella_projects'])
        self.services = conf['services']
