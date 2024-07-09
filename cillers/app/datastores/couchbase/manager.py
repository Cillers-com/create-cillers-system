from .base import get_cluster, ensure_bucket_provisioned, ensure_scope_exists

def ensure_cluster_initialized(datastore_conf, cluster_conf, client_conf):
    print(f"Ensuring Couchbase cluster is initialized")
    initialize_cluster(datastore_conf, cluster_conf, client_conf)

def ensure_metadata_initialized(datastore_conf, cluster_conf, client_conf):
    print(f"Ensuring Couchbase cluster metadata is initialized")
    cluster = get_cluster(client_conf)
    bucket_settings = generate_metadata_bucket_settings(datastore_conf, cluster_conf)
    ensure_bucket_provisioned(cluster, bucket_settings)
    ensure_scope_exists(cluster, bucket_settings.name, 'metadata')

def wait_until_ready_for_instructions(client_conf, max_retries=100, retry_delay=1, timeout_seconds=10):
    print("Connecting to Couchbase ...")
    service_types = [
            ServiceType.Management,
            ServiceType.KeyValue,
            ServiceType.Query
        ]
    timeout_option = timedelta(seconds=timeout_seconds)
    wait_until_ready_options = WaitUntilReadyOptions(service_types=service_types)
    for attempt in range(max_retries):
        try:
            cluster = get_cluster(client_conf)
            cluster.wait_until_ready(timeout_option, wait_until_ready_options)
            print("Couchbase is ready for instructions.")
            return
        except Exception as e:
            print(f"Retrying... {e}")
            time.sleep(retry_delay)
    raise Exception("Failed to connnect to Couchbase.")

def change(client_conf, data_structures_conf, metadata_conf):
    cluster = get_cluster(client_conf)
    for datastructure_key, datastructure_conf in data_structure_conf:
        change_versions_applied = get_change_versions_applied(clusters, metadata_conf, data)
        change_versions_all = get_all_change_versions()
        for version in change_versions:
            if version not in applied_changes:
                module_path = f"{directory.replace('/', '.')}.{file[:-3]}"  # Remove '.py' from filename
                migration_module = __import__(module_path, fromlist=['change'])
                migration_module.change(client_conf)
                applied_migrations.add(version)
                collection.upsert("applied_migrations", list(applied_migrations))  
                print(f"Migration {file} applied.")

def generate_metadata_bucket_settings(datastore_conf, cluster_conf):
    metadata_conf = datastore_conf['metadata']
    metadata_bucket_specs_conf = cluster_conf['metadata_bucket_specs']
    bucket_settings = BucketSettings(
            name = metadata_conf['bucket'],
            bucket_type = BucketType.COUCHBASE,
            ram_quota_mb = metadata_bucket_specs_conf['ram'],
            num_replicas = metadata_bucket_specs_conf['replicas'],
            durability_min_level = metadata_bucket_specs_conf['durability']
        )
    return bucket_settings

def get_change_versions():
    change_file_dir = '../../../changes'
    return sorted(
        [f for f in os.listdir(change_file_dir) if f.endswith('.py')],
        key=lambda x: int(x.split('.')[0])
    )

def get_applied_change_versions(cluster, metadata_conf):
    bucket_name = metadata_conf['bucket']
    scope_name = metadata_conf['scope']
    collection_name = 
    ['bucket'], metadata_conf['scope'], 'applied_changes')
        applied_changes = get_all_documents_in_collection(collection)
        collection = get_applied_changes_collection(cluster, metadata_conf)
        applied_change_versions = [key in applied_changes

