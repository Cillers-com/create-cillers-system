from config import config
from .models import init, change

def change_cluster(conf: ClusterChangeConfig):
    print(f"Couchbase change operator in progress")
    cluster = init.ensure_ready_for_change(conf)
    change.run(cluster, conf.data_structures, conf.metadata, conf.env_id)

