from . import filepaths
from .base import yaml_parser

class ConfigCillers:
    environments: list[str]
    datastores: list[str]

    def __init__(self):
        c = yaml_parser.load(filepaths.CONF)
        self.environments = c['environments']
        self.datastores = c['datastores']