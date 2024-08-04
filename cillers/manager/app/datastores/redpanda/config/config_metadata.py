class ConfigMetadata:
    _conf: dict
    prefix: str

    def __init__(self, conf: dict):
        self._conf = conf
        self.prefix = conf['prefix']

