from .config_validator_helpers import (
    assert_valid_dict,
    assert_valid_typed_dict,
    assert_list_of_strings
)

def assert_valid_data_structures(conf):
    assert isinstance(conf, dict)
    assert len(conf) > 0

def assert_valid_clusters(conf):
    assert isinstance(conf, dict)
    assert len(conf) > 0

def assert_valid(conf):
    assert_valid_dict(conf, {
        'data_structures': assert_valid_data_structures, 
        'metadata_topics_prefix': str,
        'clusters': assert_valid_clusters
    })

