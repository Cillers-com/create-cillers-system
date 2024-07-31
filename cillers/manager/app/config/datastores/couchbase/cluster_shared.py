class ServiceGroup:
    _conf: dict

    def __init__(self, conf: dict):
        self._conf = conf

class BucketSpec:
    _conf: dict
    ram: int
    replicas: int
    durability: str

    def __init__(self, conf: dict):
        self._conf = conf
        self.ram = int(conf['ram'])
        self.replicas = int(conf['replicas'])
        self.durability = conf['durability']

