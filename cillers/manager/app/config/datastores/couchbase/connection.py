from enum import Enum

class Protocol(Enum):
    COUCHBASE = 'couchbase'
    COUCHBASES = 'couchbases'

class Connection:
    _conf: dict
    protocol: Protocol
    host: str
    port: int
    connection_string: str

    def __init(self, conf: dict):
        self._conf = conf
        self.protocol = conf['protocol']
        self.host = conf['host']
        self.port = conf['port']
        self.connection_string = f"{self.protocol}://{self.host}" 
    
