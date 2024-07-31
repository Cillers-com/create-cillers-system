from . import yaml_parser

ConfigUnion = Union[dict, list, str, None]

class Standards:
    standards: dict[str, ConfigUnion] 

    def __init__(self, filepath: str):
        self.standards = yaml_parser.load(filepath)

    def get(self, standard_id):
        assert standard_id.startswith('standard_')
        key = standard_id.removeprefix("standard_")
        if key not in self.standards:
            m = f"Standard not found: '{standard}' doesn't exist in standards"
            raise KeyError(m)
        return standards[standard_id]

    def replace(conf: dict):
        if isinstance(conf, dict):
            return {key: self.replace(value) for key, value in conf.items()}
        if isinstance(conf, list):
            return [self.replace(item) for item in conf]
        if isinstance(conf, str) and conf.startswith('standard_'):
            standard_conf = self.get(conf)
            return self.replace(standard_conf)
        if not(isinstance(conf, int) or
                conf is None or
                (isinstance(conf, str) and not conf.startswith('standard_'))):
            raise ValueError("Config has element of unsupported type: '{conf}'")
        return config

