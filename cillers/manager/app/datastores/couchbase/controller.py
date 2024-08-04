from .models.model_cluster import ModelCluster
from .config_couchbase import ConfigCouchbase

class ControllerCouchbase:
    conf: ConfigCouchbase

    def __init__(self):
        self.conf = ConfigCouchbase()

    def change(self):
        print("Couchbase change in progress")
        for _, cluster_conf in self.conf.clusters_in_current_env().items():
            ModelCluster(cluster_conf).change()
