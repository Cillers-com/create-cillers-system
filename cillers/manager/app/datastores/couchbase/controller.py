from .models import init, change
from .cluster_config import CouchbaseClusterConfig

def change_cluster(cluster_id: str):
    print("Couchbase change operator in progress")
    conf = CouchbaseClusterConfig(cluster_id)
    cluster = init.ensure_ready_for_change(conf)
    change.run(cluster, conf)
