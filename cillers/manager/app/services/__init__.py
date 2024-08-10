from enum import Enum
from typing import Union
from .couchbase.controller import ControllerCouchbase
from .redpanda.controller import ControllerRedpanda

ControllerServiceUnion = Union[ControllerCouchbase]
ControllerDatastoreUnion = Union[ControllerCouchbase, ControllerRedpanda]

class ServiceId(Enum):
    COUCHBASE = 'couchbase'
    REDPANDA = 'redpanda'

controller_switch_datastores: dict[ServiceId, ControllerDatastoreUnion] = {
    ServiceId.COUCHBASE: ControllerCouchbase,
    ServiceId.REDPANDA: ControllerRedpanda
}

controller_switch_services: dict[ServiceId, ControllerServiceUnion] = {
    ServiceId.COUCHBASE: ControllerCouchbase
}

def get_controller_datastore(service_id: ServiceId) -> ControllerDatastoreUnion:
    return controller_switch_datastores[service_id]()

def get_controller_service(service_id: ServiceId) -> ControllerServiceUnion:
    return controller_switch_services[service_id]()
