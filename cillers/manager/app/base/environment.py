import os
from .. import filepaths
from . import yaml_parser

def environments() -> list[str]:
    return yaml_parser.load(filepaths.CONF)['environments']

env_id = os.getenv('ENVIRONMENT', 'development')

