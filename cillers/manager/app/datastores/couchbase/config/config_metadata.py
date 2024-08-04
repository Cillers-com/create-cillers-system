class ConfigMetadata:
    _conf: dict
    bucket: str
    scope: str

    def __init__(self, conf: dict):
        self._conf = conf
        self.bucket = conf['bucket']
        self.scope = conf['scope']

