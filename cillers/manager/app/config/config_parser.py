import os
import logging
from typing import Union
import yaml

logger = logging.getLogger(__name__)

file_paths = { 
    'standards_clients': './app/standards/clients.yml',
    'standards_datastores': './app/standards/datastores.yml',
    'config_environments': '/root/conf/environments.yml',
    'config_clients': '/root/conf/clients.yml',
    'config_datastores': '/root/conf/datastores.yml'
}

def assert_should_not_reach():
    assert False, "Branching error: Should not reach this point"

def yaml_env_constructor(loader, node):
    value = loader.construct_scalar(node)
    return os.getenv(value)

yaml.SafeLoader.add_constructor('!env', yaml_env_constructor)

def parse_yaml_file(file_path_id: str):
    assert file_path_id in file_paths
    path = file_paths[file_path_id]
    with open(path, 'r', encoding='utf-8') as file:
        data = yaml.safe_load(file)
        return data

standards = {
    'clients': parse_yaml_file('standards_clients'),
    'datastores': parse_yaml_file('standards_datastores')
}

def get_standard(standard: str, module: str, group: str) -> Union[dict, list, str]:
    assert standard.startswith('standard_')
    key = standard.removeprefix("standard_")
    if key not in standards[module][group]:
        m = f"Standard not found: '{standard}' doesn't exist in namespace '{module}.{group}'"
        raise KeyError(m)
    return standards[module][group][key]

Config = Union[dict, list, str, None]

def replace_standards(config: Config, module: str, group: str) -> Config:
    if isinstance(config, dict):
        return {key: replace_standards(value, module, group) for key, value in config.items()}
    if isinstance(config, list):
        return [replace_standards(item, module, group) for item in config]
    if isinstance(config, str) and config.startswith('standard_'):
        standard_config = get_standard(config, module, group)
        return replace_standards(standard_config, module, group)
    assert(
        isinstance(config, int) or
        config is None or
        (isinstance(config, str) and not config.startswith('standard_'))
    )
    return config

def convert_string_values_to_lists(config: dict) -> dict:
    return {key: [value] if isinstance(value, str) else value for key, value in config.items()}

def parse_environments() -> dict:
    file_config = parse_yaml_file('config_environments')
    return {key: convert_string_values_to_lists(value) for key, value in file_config.items()}

def parse_config_file_with_standards(module: str) -> dict:
    file_config = parse_yaml_file('config_' + module)
    if not isinstance(file_config, dict): 
        raise Exception("Syntax error: Only dict format allowed in top level of config")
    return {key: replace_standards(value, module, key) for key, value in file_config.items()}

def parse() -> dict:
    config = {
        "environments": parse_environments(),
        "clients": parse_config_file_with_standards('clients'),
        "datastores": parse_config_file_with_standards('datastores')
    }
    return config
