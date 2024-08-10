from ..enums.cloud_provider_cloud import CloudProviderCloud

class ConfigCloud:
    _conf: dict
    provider: CloudProviderCloud
    region: str

    def __init__(self, conf: dict):
        self._conf = conf
        self.provider = conf['provider']
        self.region = conf['region']

