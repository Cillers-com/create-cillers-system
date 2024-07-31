from enum import Enum

class CredentialType(Enum):
    BASIC = 'basic'

class BasicCredentials:
    _conf: dict
    username: str
    password: str

    def __init__(self, conf: dict):
        self._conf = conf
        self.username: conf['username']
        self.password: conf['password']

CredentialsUnion = Union[CredentialsBasic]

class Credentials:
    _conf: dict
    credentials: dict(str, CredentialsUnion)

    def __init__(self, conf: dict):
        self._conf = conf
        self.credentials = {}
        for key, credentials in credentials.items():
            if credentials['type'] == CredentialsType.BASIC:
                self.credentials[key] = CredentialsBasic(credentials)
            else:
                raise KeyError(f"Unknown credentials type '{credentials['type']}'")

