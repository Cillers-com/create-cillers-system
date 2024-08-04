from enum import Enum
from typing import Union
from types import ModuleType
from .couchbase.controller import ControllerCouchbase
from .redpanda.controller import ControllerRedpanda

ControllerDatastoreUnion = Union[ControllerCouchbase, ControllerRedpanda]

class DatastoreId(Enum):
    COUCHBASE = 'couchbase'
    REDPANDA = 'redpanda'

controller_switch = {
    DatastoreId.COUCHBASE: ControllerCouchbase,
    DatastoreId.REDPANDA: ControllerRedpanda
}

def get_controller(datastore_id: DatastoreId) -> ControllerDatastoreUnion:
    return controller_switch[datastore_id]()
