from config import config
from .models import init, change

def change_cluster(conf: ClusterChangeConfig):
    print(f"Redpanda change operator in progress")
    admin_client = init.ensure_ready_for_change(conf, 5*60)
    change.run(admin_client, conf.data_structures, conf.metadata)

