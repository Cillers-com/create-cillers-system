from config import config
from .models import init, change
from .cluster_change_config import RedpandaClusterConfig

def change_cluster(cluster_id: str):
    print(f"Redpanda change operator in progress")
    conf = config.ClusterChangeConfig('redpanda', cluster_id)
    admin_client = init.ensure_ready_for_change(conf, 5*60)
    change.run(conf)

