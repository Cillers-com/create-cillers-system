from . import (
    config_validator_couchbase,
    config_validator_redpanda
)
from .config_validator_helpers import (
    assert_valid_dict
)

def assert_valid_module(module, conf):
    config_validators = { 
        'couchbase': config_validator_couchbase,
        'redpanda': config_validator_redpanda
    }
    config_validators[module].assert_valid(conf)

def assert_valid(conf):
    assert isinstance(conf, dict)
    assert len(conf) > 0
    assert_valid_dict(conf, { 
        'couchbase?': dict, 
        'redpanda?': dict
    })
    for module, module_conf in conf.items():
        assert_valid_module(module, module_conf)

