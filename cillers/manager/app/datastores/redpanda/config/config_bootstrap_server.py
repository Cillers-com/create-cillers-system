class ConfigBootstrapServer:
    host: str
    port: int
    
    def __init__(self, conf: dict):
        self.host = conf['host']
        self.port = conf['port']
