from ..enums.protocol import Protocol

class ConfigConnection:
    _conf: dict
    protocol: Protocol
    host: str
    port: int

    def __init__(self, conf: dict):
        self._conf = conf
        self.protocol = conf['protocol']
        self.host = conf['host']
        self.port = conf['port']
