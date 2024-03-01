import os

from . import http_server

def get_http_port() -> int | None:
    if port :=  os.environ.get('HTTP_PORT'):
        try:
            return int(port)
        except ValueError:
            return None

def get_http_host() -> str:
    return os.environ.get('HTTP_HOST', '0.0.0.0')

def get_http_debug() -> bool:
    return os.environ.get('HTTP_DEBUG', 'false').lower() == 'true'

def get_http_autoreload() -> bool:
    return os.environ.get('HTTP_AUTORELOAD', 'false').lower() == 'true'

def get_http_graphql_ui() -> bool:
    return os.environ.get('HTTP_GRAPHQL_UI', 'false').lower() == 'true'

def get_http_conf() -> http_server.ServerConf:
    return http_server.ServerConf(
        port=int(get_http_port()),
        host=get_http_host(),
        debug=get_http_debug(),
        autoreload=get_http_autoreload()
    )

def validate():
    if not get_http_port():
        return False
    return True
