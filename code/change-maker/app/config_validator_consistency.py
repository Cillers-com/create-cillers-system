
def assert_active_clusters_have_conf(environments, data_stores):
    for env, env_conf in environments.items():
        for module, clusters in env_conf.items():
            for cluster in clusters.items():
                assert cluster in data_stores[module]['clusters']

def assert_active_change_maker_clients_have_conf(data_stores, clients):
    for module_id, module_conf in data_stores.items():
        for instance_id, instance_conf in module_conf['clusters'].items():
            client_path = instance_conf['change_maker_client']
            module, instance, client = client_path.split('.')
            assert module in clients
            assert instance in clients[module]
            assert client in clients[module][instance]['credentials'][client]

def assert_valid(environments, clients, data_stores):
    assert_active_clusters_have_conf(environments, data_stores)
    assert_active_change_maker_clients_have_conf(data_stores, clients)
