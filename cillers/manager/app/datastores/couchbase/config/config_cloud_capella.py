from ..enums.cloud_provider_capella import CloudProviderCapella

class ConfigCloudCapella:
    _conf: dict
    provider: CloudProviderCapella
    region: str

    def __init__(self, conf: dict):
        self._conf = conf
        self.provider = conf['provider']
        self.region = conf['region']

