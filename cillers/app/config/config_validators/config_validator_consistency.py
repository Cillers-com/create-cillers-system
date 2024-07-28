
def assert_active_clusters_have_conf(environments, datastores):
    for _, env_conf in environments.items():
        for module, clusters in env_conf.items():
            for cluster in clusters:
                assert cluster in datastores[module]['clusters']

def assert_active_change_maker_clients_have_conf(datastores, clients):
    for _, module_conf in datastores.items():
        for _, instance_conf in module_conf['clusters'].items():
            client_path = instance_conf['change_maker_client']
            module, instance, client = client_path.split('.')
            assert module in clients
            assert instance in clients[module]
            client_module = clients[module]
            assert instance in client_module
            client_module_instance_credentials = client_module[instance]['credentials']
            assert client in client_module_instance_credentials

def assert_valid(environments, clients, datastores):
    assert_active_clusters_have_conf(environments, datastores)
    assert_active_change_maker_clients_have_conf(datastores, clients)
