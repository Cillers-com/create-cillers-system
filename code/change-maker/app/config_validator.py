from . import (
    config_validator_clients, 
    config_validator_environemnts,
    config_validator_data_stores,
    config_validator_consistency
)

def assert_valid(conf):
    assert set(conf.keys()) == set(['environments', 'clients', 'data_stores'])

    environments = conf['environments']
    clients = conf['clients']
    data_stores = conf['data_stores']

    config_validator_environments.assert_valid(environments)
    config_validator_clients.assert_valid(clients)
    config_validator_data_stores.assert_valid(data_stores)
    config_validator_consistency.assert_valid(environments, clients, data_stores)

