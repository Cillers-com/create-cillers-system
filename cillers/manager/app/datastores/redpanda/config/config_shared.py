from .config_data_structures import ConfigDataStructureUnion, generate_data_structures
from .config_metadata import ConfigMetadata

class ConfigShared:
    _conf: dict
    metadata: ConfigMetadata
    data_structures: dict[str, ConfigDataStructureUnion]

    def __init__(self, conf: dict):
        self._conf = conf
        self.metadata = ConfigMetadata(conf['metadata'])
        self.data_structures = generate_data_structures(conf['data_structures'])
