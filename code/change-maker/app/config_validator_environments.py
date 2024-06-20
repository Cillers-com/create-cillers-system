from .config_validator_helpers import (
    assert_subdicts_have_same_keys,
    assert_list_of_strings
)

def assert_valid(conf):
    assert isinstance(conf, dict)
    assert len(conf) > 0
    assert_subdicts_have_same_keys(conf)
    for environment, data_stores in conf.items():
        for module, clusters in data_stores.items(): 
            assert module in {'couchbase', 'redpanda'}
            assert_list_of_strings(clusters) 

