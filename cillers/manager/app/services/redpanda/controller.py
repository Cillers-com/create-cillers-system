from .models.model_cluster import ModelCluster
from .config_redpanda import ConfigRedpanda

class ControllerRedpanda:
    conf: ConfigRedpanda

    def __init__(self):
        self.conf = ConfigRedpanda()

    def change(self):
        print("Redpanda change in progress")
        for _, cluster_conf in self.conf.clusters_in_current_env().items():
            ModelCluster(cluster_conf).change()
