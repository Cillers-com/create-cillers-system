from .config_bootstrap_server import ConfigBootstrapServer

class ConfigConnection:
    _conf: dict
    bootstrap_servers: list[ConfigBootstrapServer]
    security_protocol: str | None
    ssl_ca_location: str | None
    ssl_certificate_location: str | None
    ssl_key_location: str | None

    def __init__(self, conf: dict):
        self._conf = conf
        self.bootstrap_servers = [ConfigBootstrapServer(c) for c in conf['bootstrap_servers']]
        self.security_protocol = conf['security_protocol']
        self.ssl_ca_location = conf['ssl_ca_location']
        self.ssl_certificate_location = conf['ssl_certificate_location']
        self.ssl_key_location = conf['ssl_key_location']
