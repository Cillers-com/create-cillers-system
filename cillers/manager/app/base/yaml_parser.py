import os
from pathlib import Path
import yaml

def yaml_env_constructor(loader, node):
    value = loader.construct_scalar(node)
    return os.getenv(value)

yaml.SafeLoader.add_constructor('!env', yaml_env_constructor)

def load(filepath: Path):
    with open(filepath, 'r', encoding='utf-8') as file:
        data = yaml.safe_load(file)
    return data

