from pathlib import Path
import importlib.util
import inspect
import json
from typing import List, Dict, Callable
from kafka import KafkaProducer, KafkaConsumer

class DataStructureDirectory:
    path: Path
    key: str
    
    def __init__(self, key: str):
        self.key = key
        self.path = Path('/root/change/redpanda') / key

    def all_ids(self) -> List[str]:
        return [f.stem for f in self.path.rglob('*.py')]

    def change_function(self, id: str) -> Callable:
        filepath = self.path / f"{id}.py"
        assert filepath.exists()
        spec = importlib.util.spec_from_file_location(id, filepath)
        module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)
        if not hasattr(module, 'change'):
            raise Exception(f"Change module 'redpanda.{self.key}.{id}' has no function 'change'")
        function = getattr(module, 'change')
        if not callable(function):
            raise Exception(f"The 'change' attribute in module 'redpanda.{self.key}.{id}' is not callable")
        return function

class DataStructureTopic:
    key: str
    topic_name: str
    bootstrap_servers: List[str]

    def __init__(self, key: str, bootstrap_servers: str, metadata_conf: Dict):
        self.key = key
        self.topic_name = metadata_conf['topic']
        self.boot

    def applied_ids(self) -> List[str]:
        consumer = KafkaConsumer(
            self.topic_name,
            bootstrap_servers=[self.bootstrap_servers],
            auto_offset_reset='earliest',
            value_deserializer=lambda m: json.loads(m.decode('utf-8'))
        )
        consumer.subscribe([self.topic_name])
        ids = []
        for message in self.consumer:
            ids.append(message.value['id'])
            if message.offset == consumer.end_offsets([message.partition]) - 1:
                break
        consumer.close()
        return ids

    def set_applied(self, id: str, change_fn: Callable):
        producer = KafkaProducer(
            bootstrap_servers=[self.bootstrap_servers],
            value_serializer=lambda m: json.dumps(m).encode('utf-8')
        )
        code = inspect.getsource(change_fn)
        message = {'id': id, 'code': code}
        producer.send(self.topic_name, message)
        producer.flush()
        producer.close()

class DataStructure:
    directory: DataStructureDirectory
    topic: DataStructureTopic
    type: str
    conf: Dict
    connection_conf: Dict
    credentials_conf: Dict

    def __init__(self, connection_conf: Dict, credentials_conf: Dict, key: str, conf: Dict, metadata_conf: Dict):
        self.directory = DataStructureDirectory(key)
        self.topic = DataStructureTopic(key, self['connections_conf']['bootstrap_servers'], metadata_conf)
        self.type = conf['type']
        self.conf = conf
        self.connection_conf = connection_conf
        self.credentials_conf = credentials_conf
        
    def change(self):
        if self.type == 'cluster':
            self.change_cluster()
        elif self.type == 'prefix_clones':
            self.change_prefix_clones()
        else:
            raise Exception(f"Type error '{self.type}'")

    def change_cluster(self):
        ids = self.to_apply_ids()
        sorted_ids = sorted(ids, key=lambda x: int(x.split('-')[0]))
        for id in sorted_ids:
            change_function = self.directory.change_function(id)
            change_function(self.get_connection_settings())
            self.topic.set_applied(id, change_function)

    def get_connection_settings():
        settings = {
            'bootstrap_servers': self.connection['bootstrap_servers'],
            'client_id': 'change'
        }
        if self.credentials:
            mechanism = self.connection['sasl_mechanism']
            settings['security_protocol'] = self.connection['security_protocol']
            settings['sasl_mechanism'] = mechanism
            if mechansim in ['PLAIN', 'SCRAM-SHA-256', 'SCRAM-SHA-512']:
                settings['sasl.username'] = self.credentials['username']
                settings['sasl.password'] = self.credentials['password']
            elsif mechanism == 'GSSAPI':
                settings['kerberos.service.name'] = self.credentials['kerberos_service_name']
            elsif mechanism == 'OAUTHBEARER':
                raise Exception('OAUTHBEARER is not yet implemented')
                settings['sasl.oauthbearer.config'] = self.credentials['oauthbearer_token_provider']
        return settings

    def change_prefix_clones(self):
        raise NotImplementedError("Not yet implemented")

    def to_apply_ids(self) -> List[str]:
        all_ids = self.directory.all_ids()
        applied_ids = self.topic.applied_ids()
        return [id for id in all_ids if id not in applied_ids]

def run(bootstrap_servers: str, data_structures_conf: Dict, metadata_conf: Dict):
    for key, conf in data_structures_conf.items():
        DataStructure(bootstrap_servers, key, conf, metadata_conf).change()

