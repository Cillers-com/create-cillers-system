class ConfigClusterSpecLocal:
    _conf: dict
    ram: int
    index_ram: int
    fts_ram: int

    def __init__(self, conf: dict):
        self._conf = conf
        self.ram = conf['ram']
        self.index_ram = conf['index_ram']
        self.fts_ram = conf['fts_ram']

