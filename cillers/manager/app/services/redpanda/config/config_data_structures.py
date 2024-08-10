from typing import Union
from ..enums.type_data_structure import TypeDataStructure

class ConfigDataStructureCluster:
    _conf: dict
    topic_prefixes_to_exclude: list[str]

    def __init__(self, conf: dict):
        self._conf = conf
        self.type = TypeDataStructure.CLUSTER
        self.topic_prefixes_to_exclude = conf.get('topic_prefixes_to_exclude', [])

class ConfigDataStructureTopicClones:
    _conf: dict
    prefix: str

    def __init__(self, conf: dict):
        self._conf = conf
        self.type = TypeDataStructure.TOPIC_CLONES
        self.prefix = conf['prefix']

ConfigDataStructureUnion = Union[
        ConfigDataStructureCluster,
        ConfigDataStructureTopicClones]

class_switch = {
    TypeDataStructure.CLUSTER: ConfigDataStructureCluster,
    TypeDataStructure.TOPIC_CLONES: ConfigDataStructureTopicClones}

def generate_data_structures(conf: dict) -> dict[str, ConfigDataStructureUnion]:
    data_structures = {}
    for ds_id, ds_conf in conf['data_structures'].items():
        data_structures[ds_id] = class_switch[ds_id](ds_conf)
    return data_structures

