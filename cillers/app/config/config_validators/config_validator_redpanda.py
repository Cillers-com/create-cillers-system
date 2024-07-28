from .config_validator_helpers import assert_valid_dict

def assert_valid_data_structures(conf):
    assert isinstance(conf, dict)
    assert len(conf) > 0

def assert_valid_clusters(conf):
    assert isinstance(conf, dict)
    assert len(conf) > 0

def assert_valid_metadata(conf):
    assert_valid_dict(conf, {
        'topics_prefix': str
    })

def assert_valid(conf):
    assert_valid_dict(conf, {
        'data_structures': assert_valid_data_structures, 
        'metadata': assert_valid_metadata,
        'clusters': assert_valid_clusters
    })
