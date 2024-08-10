from ...base import yaml_parser
from ...base.standards import Standards
from . import filepaths
from .config.config_shared import ConfigShared
from .config.config_clusters import ConfigClusters, ConfigClusterUnion

class ConfigRedpanda:
    _conf: dict
    shared: ConfigShared
    clusters: ConfigClusters

    def __init__(self):
        conf_loaded = yaml_parser.load(filepaths.CONF)
        conf = Standards(filepaths.STANDARDS).replace(conf_loaded)
        self._conf = conf
        self.shared = ConfigShared(conf['shared'])
        self.clusters = ConfigClusters(conf['clusters'], self.shared)

    def clusters_in_current_env(self) -> dict[str, ConfigClusterUnion]:
        return self.clusters.get_in_current_env()

