from typing import Union
from ..enums.type_credentials import TypeCredentials

class ConfigCredentialsBasic:
    _conf: dict
    username: str
    password: str

    def __init__(self, conf: dict):
        self._conf = conf
        self.username = conf['username']
        self.password = conf['password']

ConfigCredentialsUnion = Union[ConfigCredentialsBasic]

def generate_credentials(conf: dict):
    credentials = {}
    for c_id, c_conf in conf.items():
        if c_conf['type'] == TypeCredentials.BASIC:
            credentials[c_id] = ConfigCredentialsBasic(c_conf)
        else:
            raise KeyError(f"Unknown credentials type '{c_conf['type']}'")
    return credentials

class ConfigCredentials:
    _conf: dict
    credentials: dict[str, ConfigCredentialsUnion]

    def __init__(self, conf: dict):
        self._conf = conf
        self.credentials = generate_credentials(conf)

    def get(self, credentials_id) -> ConfigCredentialsUnion:
        return self.credentials[credentials_id]
