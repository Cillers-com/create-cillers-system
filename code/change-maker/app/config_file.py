import os
import logging
import yaml

logger = logging.getLogger(__name__)

def env_constructor(loader, node):
    value = loader.construct_scalar(node)
    return os.getenv(value)

yaml.SafeLoader.add_constructor('!env', env_constructor)

def initial_parse(file_path):
    with open(file_path, 'r') as file:
        try:
            data = yaml.safe_load(file)
            return data
        except yaml.YAMLError as exc:
            print(f"Error parsing YAML file {file_path}: {exc}")

