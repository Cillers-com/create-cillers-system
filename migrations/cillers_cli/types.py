from typing import Annotated, Any, List, Literal

from pydantic import BaseModel, Field, TypeAdapter, validate_arguments

from . import log, couchbase, kafka, kafka_connect

logger = log.get_logger(__name__)

#### Types ####

## Base ##

class ConnectionConfs(BaseModel):
    kafka: kafka.ConnectionConf
    kafka_connect: kafka_connect.ConnectionConf
    couchbase: couchbase.ConnectionConf

class OpBase(BaseModel):
    def apply(self, conf: ConnectionConfs) -> None:
        raise NotImplementedError

    def revert(self, conf: ConnectionConfs) -> None:
        raise NotImplementedError

## Topics ##

class CreateTopicOp(OpBase):
    type: Literal['create-topic'] = 'create-topic'
    spec: kafka.TopicSpec

    def apply(self, conf: ConnectionConfs) -> None:
        kafka.create_topic(conf.kafka, self.spec)

    def revert(self, conf: ConnectionConfs) -> None:
        kafka.delete_topic(conf.kafka, self.spec.name)

class ModifyTopicOp(OpBase):
    type: Literal['modify-topic'] = 'modify-topic'
    spec: kafka.TopicSpec  # TODO: partial updates allowed

    def apply(self, conf: ConnectionConfs) -> None:
        kafka.modify_topic(conf.kafka, self.spec)

    def revert(self, conf: ConnectionConfs) -> None:
        raise NotImplementedError

class DeleteTopicOp(OpBase):
    type: Literal['delete-topic'] = 'delete-topic'
    name: str

    def apply(self, conf: ConnectionConfs) -> None:
        kafka.delete_topic(conf.kafka, self.name)
        raise NotImplementedError

    def revert(self, conf: ConnectionConfs) -> None:
        raise NotImplementedError

## Buckets ##

class CreateBucketOp(OpBase):
    type: Literal['create-bucket'] = 'create-bucket'
    spec: couchbase.BucketSpec

    def apply(self, conf: ConnectionConfs) -> None:
        couchbase.ensure_bucket_exists(conf.couchbase, self.spec)

    def revert(self, conf: ConnectionConfs) -> None:
        couchbase.delete_bucket(conf.couchbase, self.spec.name)

class ModifyBucketOp(OpBase):
    type: Literal['modify-bucket'] = 'modify-bucket'
    name: str

    def apply(self, conf: ConnectionConfs) -> None:
        couchbase.ensure_bucket_exists(conf.couchbase, self.spec)

    def revert(self, conf: ConnectionConfs) -> None:
        raise NotImplementedError

class DeleteBucketOp(OpBase):
    type: Literal['delete-bucket'] = 'delete-bucket'
    name: str

    def apply(self, conf: ConnectionConfs) -> None:
        couchbase.delete_bucket(conf.couchbase, self.spec.name)

    def revert(self, conf: ConnectionConfs) -> None:
        raise NotImplementedError

## Collections ##

class CreateCollectionOp(OpBase):
    type: Literal['create-collection'] = 'create-collection'
    spec: couchbase.CollectionSpec

    def apply(self, conf: ConnectionConfs) -> None:
        couchbase.ensure_collection_exists(conf.couchbase, self.spec)

    def revert(self, conf: ConnectionConfs) -> None:
        couchbase.delete_collection(conf.couchbase, self.spec.name)

class DeleteCollectionOp(OpBase):
    type: Literal['delete-collection'] = 'delete-collection'
    name: str

    def apply(self, conf: ConnectionConfs) -> None:
        couchbase.delete_collection(conf.couchbase, self.spec.name)

    def revert(self, conf: ConnectionConfs) -> None:
        raise NotImplementedError

## Connectors ##

class CreateConnectorOp(OpBase):
    type: Literal['create-connector'] = 'create-connector'
    spec: kafka_connect.ConnectorSpec

    def apply(self, conf: ConnectionConfs) -> None:
        kafka_connect.ensure_connector_exists(conf.kafka_connect, self.spec)

    def revert(self, conf: ConnectionConfs) -> None:
        kafka_connect.delete_connector(conf.kafka_connect, self.spec.name)

class ModifyConnectorOp(OpBase):
    type: Literal['modify-connector'] = 'modify-connector'
    spec: kafka_connect.ConnectorSpec

    def apply(self, conf: ConnectionConfs) -> None:
        kafka_connect.modify_connector(conf.kafka_connect, self.spec)

    def revert(self, conf: ConnectionConfs) -> None:
        raise NotImplementedError

class DeleteConnectorOp(OpBase):
    type: Literal['delete-connector'] = 'delete-connector'
    name: str

    def apply(self, conf: ConnectionConfs) -> None:
        kafka_connect.delete_connector(conf.kafka_connect, self.name)

    def revert(self, conf: ConnectionConfs) -> None:
        raise NotImplementedError

Op = Annotated[CreateBucketOp
               | CreateCollectionOp
               | CreateConnectorOp
               | CreateTopicOp
               | DeleteBucketOp
               | DeleteCollectionOp
               | DeleteConnectorOp
               | DeleteTopicOp
               | ModifyBucketOp
               | ModifyConnectorOp
               | ModifyTopicOp,
               Field(discriminator='type')]

class MigrationFile(BaseModel):
    ops: list[dict[str, Any]]

class Migration(BaseModel):
    id: str
    ops: list[Op]

#### Utils ####

@validate_arguments
def parse(data: MigrationFile) -> list[Op]:
    return TypeAdapter(List[Op]).validate_python(data.ops)
