from .config_validator_helpers import (
    assert_valid_dict,
    assert_valid_typed_dict
)

def assert_valid_connection(conf):
    assert_valid_dict(conf, {
        'protocol': str,
        'host': str,
        'port?': int
    })

def assert_valid_credentials_instance(conf):
    assert_valid_typed_dict(conf, {
        'api_key': {
            'api_key': str,
            'secret': str
        }, 
        'basic': {
            'username': str,
            'password': str
        }
    })

def assert_valid_credentials(conf):
    for instance_id, instance_conf in conf.items():
        assert_valid_credentials_instance(instance_conf)

def assert_valid(conf):
    assert isinstance(conf, dict)
    assert len(conf) > 0
    for module_id, module_conf in conf.items():
        assert isinstance(module_conf, dict)
        for instance_id, instance_conf in module_conf.items():
            assert_valid_dict(instance_conf, {
                'connection': dict, 
                'credentials': dict
            })
            assert_valid_connection(instance_conf['connection'])
            assert_valid_credentials(instance_conf['credentials'])
            
