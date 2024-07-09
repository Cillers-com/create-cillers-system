from .config_validator_helpers import (
    assert_valid_dict,
    assert_valid_typed_dict,
    assert_list_of_strings
)

def assert_valid_data_structures(conf):
    assert isinstance(conf, dict)
    assert len(conf) > 0
    for key, data_structure_conf in conf.items():
        assert_valid_typed_dict(data_structure_conf, {
            'couchbase_cluster': {
                'bucket_prefixes_to_exclude?': assert_list_of_strings,
                'scope_prefixes_to_exclude?': assert_list_of_strings
            }, 
            'couchbase_bucket_clones': {
                'prefix': str
            },
            'couchbase_scope_clones': {
                'prefix': str,
                'bucket': str
            }
        })

def assert_valid_capella_nodes(conf):
    assert isinstance(conf, int)
    assert 3 <= conf <= 100

def assert_valid_capella_disk_storage(conf):
    assert isinstance(conf, int)
    assert conf in [50]

def assert_valid_capella_disk_type(conf):
    assert isinstance(conf, str)
    assert conf in ['gp3']

def assert_valid_capella_disk_iops(conf):
    assert isinstance(conf, int)
    assert conf in [3000]

def assert_valid_capella_cpu(conf):
    assert isinstance(conf, int)
    assert conf in [16]

def assert_valid_capella_ram(conf):
    assert isinstance(conf, int)
    assert conf in [32]

def assert_valid_capella_disk(conf):
    assert_valid_dict(conf, {
        'storage': assert_valid_capella_disk_storage,
        'type': assert_valid_capella_disk_type,
        'iops': assert_valid_capella_disk_iops
    })

def assert_valid_capella_service_groups(conf):
    for key, group_conf in conf.items():
        assert_valid_dict(group_conf, {
            'services': assert_valid_services,
            'nodes': assert_valid_capella_nodes,
            'cpu': assert_valid_capella_cpu,
            'ram': assert_valid_capella_ram,
            'disk': assert_valid_capella_disk
        })
    
def assert_valid_capella_region_aws(conf):
    assert isinstance(conf, str)
    assert conf in {'eu-central-1'}

def assert_valid_capella_region_gcp(conf):
    assert isinstance(conf, str)
    assert conf in {'eu-central-1'}

def assert_valid_capella_region_azure(conf):
    assert isinstance(conf, str)
    assert conf in {'eu-central-1'}

def assert_valid_capella_cloud(conf):
    assert_valid_typed_dict(conf, {
        'aws': {
            'region': assert_valid_capella_region_aws
        }, 
        'gcp': {
            'region': assert_valid_capella_region_gcp
        }, 
        'azure': {
            'region': assert_valid_capella_region_azure
        }
    })

def assert_valid_services(conf):
    assert isinstance(conf, list)
    assert not set(conf) - set(['kv', 'index', 'n1ql', 'fts', 'cbas', 'eventing'])

def assert_valid_capella_node_size(conf):
    assert isinstance(conf, str)
    assert conf in {'small', 'medium', 'large'}

def assert_valid_capella_service_tier(conf):
    assert isinstance(conf, str)
    assert conf in {'developer_pro'}

def assert_valid_auto_failover_timeout(conf):
    assert isinstance(conf, int)
    assert 0 <= conf <= 60

def assert_valid_cluster_ram(conf):
    assert isinstance(conf, int)
    assert conf in {256, 512, 1024, 2048, 4096}

def assert_valid_index_ram(conf):
    assert isinstance(conf, int)
    assert conf in {256, 512, 1024, 2048, 4096}

def assert_valid_fts_ram(conf):
    assert isinstance(conf, int)
    assert conf in {256, 512, 1024, 2048, 4096}

def assert_valid_cluster_specs(conf):
    assert_valid_typed_dict(conf, {
        'capella_multi_node': {
            'size': assert_valid_capella_node_size,
            'service_tier': assert_valid_capella_service_tier,
            'auto_failover': bool,
            'auto_failover_timeout': assert_valid_auto_failover_timeout
        },
        'single_node': {
            'ram': assert_valid_cluster_ram,  
            'index_ram': assert_valid_index_ram,
            'fts_ram': assert_valid_fts_ram
        }
    })

def assert_valid_bucket_ram(conf):
    assert isinstance(conf, int)
    assert conf in {256, 512, 1024, 2048, 4096}

def assert_valid_bucket_replicas(conf):
    assert isinstance(conf, int)
    assert 0 <= conf <= 5

def assert_valid_bucket_durability(conf):
    assert isinstance(conf, str)
    assert conf in {'majority', 'none'}

def assert_valid_bucket_type(conf):
    assert isinstance(conf, str)
    assert conf in {'couchbase', 'memcached', 'ephemeral'}

def assert_valid_metadata_bucket_specs(conf):
    assert_valid_dict(conf, {
        'ram': assert_valid_bucket_ram,
        'replicas': assert_valid_bucket_replicas,
        'durability': assert_valid_bucket_durability
    })

def assert_valid_metadata(conf):
    assert_valid_dict(conf, {
        'bucket': str,
        'scope': str
    })

def assert_valid_clusters(conf):
    assert isinstance(conf, dict)
    assert len(conf) > 0
    for key, cluster_conf in conf.items():
        assert_valid_typed_dict(cluster_conf, {
            'capella': {
                'service_groups': assert_valid_capella_service_groups,
                'capella_project': str,
                'cloud': assert_valid_capella_cloud
            }, 
            'polytope_local': {
                'module': str
            }}, {
                'change_maker_client': str,
                'specs': assert_valid_cluster_specs,
                'metadata_bucket_specs': assert_valid_metadata_bucket_specs,
        })
    
def assert_valid_capella_projects(conf):
    assert isinstance(conf, dict)
    assert len(conf) > 0

def assert_valid(conf):
    assert_valid_dict(conf, {
        'metadata': assert_valid_metadata, 
        'data_structures': assert_valid_data_structures,
        'services': assert_valid_services,
        'capella_projects?': assert_valid_capella_projects, 
        'clusters': assert_valid_clusters
    })

