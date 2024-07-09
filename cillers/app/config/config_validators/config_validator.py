from . import (
    config_validator_clients, 
    config_validator_environments,
    config_validator_datastores,
    config_validator_consistency
)

def assert_valid(conf):
    assert set(conf.keys()) == set(['environments', 'clients', 'datastores'])

    environments = conf['environments']
    clients = conf['clients']
    datastores = conf['datastores']

    config_validator_environments.assert_valid(environments)
    config_validator_clients.assert_valid(clients)
    config_validator_datastores.assert_valid(datastores)
    config_validator_consistency.assert_valid(environments, clients, datastores)

