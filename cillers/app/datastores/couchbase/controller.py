from .models import cluster, change

def change_cluster(conf: ClusterChangeConfig):
    print(f"Couchbase change operator in progress")
    cluster.ensure_ready_for_change(conf.client, 5*60)
    change.run(conf)

