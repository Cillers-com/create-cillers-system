from . import parse_yaml_file, filepaths

def environments():
    parse_yaml_file(filepaths['config_cillers'])['environments']

EnvironmentId = Enum('EnvironmentId', {env.upper(): env for env in environments()})

