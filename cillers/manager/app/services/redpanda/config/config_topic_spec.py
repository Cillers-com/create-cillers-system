class ConfigTopicSpec:
    _conf: dict
    partitions: int
    replication_factor: int

    def __init__(self, conf: dict):
        self._conf = conf
        self.partitions = conf['partitions']
        self.replication_factor = conf['replication_factor']
