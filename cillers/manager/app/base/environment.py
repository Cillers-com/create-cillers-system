import os
from .. import filepaths
from . import yaml_parser

def environments() -> list[str]:
    return yaml_parser.load(filepaths.CONF)['environments']

ENV_ID = os.getenv('ENVIRONMENT', 'development')

