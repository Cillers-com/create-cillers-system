from pathlib import Path
import importlib.util
import inspect
import json
from typing import Callable
from kafka import KafkaProducer, KafkaConsumer
from ..cluster_config import RedpandaClusterConfig

class DataStructureDirectory:
    path: Path
    data_structure_id: str
    
    def __init__(self, data_structure_id: str):
        self.data_structure_id = data_structure_id 
        self.path = Path('/root/change/redpanda') / data_structure_id 

    def all_ids(self) -> list[str]:
        return [f.stem for f in self.path.rglob('*.py')]

    def change_function(self, change_id: str) -> Callable:
        filepath = self.path / f"{change_id}.py"
        assert filepath.exists()
        spec = importlib.util.spec_from_file_location(id, filepath)
        module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)
        if not hasattr(module, 'change'):
            m = (f"Change module 'redpanda.{self.data_structure_id}.{change_id}' "
                "has no function 'change'")
            raise Exception(m)
        function = getattr(module, 'change')
        if not callable(function):
            m = (f"The 'change' attribute in module 'redpanda.{self.data_structure_id}."
                 "{change_id}' is not callable")
            raise Exception(m)
        return function

class DataStructureTopic:
    data_structure_id: str
    topic_name: str
    client_params: dict

    def __init__(self, data_structure_id: str, client_params: dict, metadata_conf: dict):
        self.data_structure_id = data_structure_id
        self.client_params = client_params
        self.topic_name = metadata_conf['topic']

    def applied_ids(self) -> list[str]:
        params = {
                **self.client_params,
                'auto_offset_reset': 'earliest',
                'value_deserializer': lambda m: json.loads(m.decode('utf-8'))
        }
        consumer = KafkaConsumer(self.topic_name, **params)
        consumer.subscribe([self.topic_name])
        ids = []
        for message in consumer:
            ids.append(message.value['id'])
            if message.offset == consumer.end_offsets([message.partition]) - 1:
                break
        consumer.close()
        return ids

    def set_applied(self, change_id: str, change_fn: Callable):
        params = {
            **self.client_params,
            'value_serializer': lambda m: json.dumps(m).encode('utf-8')
        }
        producer = KafkaProducer(**params)
        code = inspect.getsource(change_fn)
        message = {'id': change_id, 'code': code}
        producer.send(self.topic_name, message)
        producer.flush()
        producer.close()

class DataStructure:
    directory: DataStructureDirectory
    topic: DataStructureTopic
    type: str
    conf: RedpandaClusterConfig 

    def __init__(self, data_structure_id: str, conf: RedpandaClusterConfig):
        self.directory = DataStructureDirectory(data_structure_id)
        self.topic = DataStructureTopic(data_structure_id, conf.client_params_change, conf.metadata)
        self.conf = conf
        self.type = conf.data_structure_type(data_structure_id)

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
        for change_id in sorted_ids:
            change_function = self.directory.change_function(change_id)
            num_params = len(inspect.signature(change_function).parameters)
            if num_params == 1:
                change_function(self.conf.client_params_change)
            elif num_params == 2:
                change_function(self.conf.client_params_change, self.conf.env_id)
            else:
                raise Exception("Change functions must take 1 or 2 parameters")
            self.topic.set_applied(change_id, change_function)

    def change_prefix_clones(self):
        raise NotImplementedError("Not yet implemented")

    def to_apply_ids(self) -> list[str]:
        all_ids = self.directory.all_ids()
        applied_ids = self.topic.applied_ids()
        return [id for id in all_ids if id not in applied_ids]

def run(conf: RedpandaClusterConfig):
    for data_structure_id in conf.data_structures:
        DataStructure(data_structure_id, conf).change()
