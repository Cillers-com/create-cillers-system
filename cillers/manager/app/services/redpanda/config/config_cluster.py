from ...shared.config.config_credentials import ConfigCredentials
from .config_shared import ConfigShared
from .config_connection import ConfigConnection
from .config_topic_spec import ConfigTopicSpec

class ConfigCluster:
    shared: ConfigShared
    credentials_id_change: str
    topic_settings_metadata: ConfigTopicSpec
    connection: ConfigConnection
    credentials: ConfigCredentials

    def __init__(self, conf: dict, shared: ConfigShared):
        self.shared = shared
        self.credentials_id_change = conf['credentials_id_change']
        self.topic_settings_metadata = ConfigTopicSpec(conf['topic_spec_metadata'])
        self.connection = ConfigConnection(conf['connection'])
        self.credentials = ConfigCredentials(conf['credentials'])
