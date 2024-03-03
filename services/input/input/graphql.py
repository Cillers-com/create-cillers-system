from functools import cached_property
import json
import strawberry
from strawberry.fastapi import BaseContext, GraphQLRouter
from strawberry.permission import BasePermission
from strawberry.types import Info as _Info
from strawberry.types.info import RootValueType
import logging
import uuid
from confluent_kafka import Producer

from . import auth

logger = logging.getLogger(__name__)

#### Context ####

class Context(BaseContext):
    @cached_property
    def user(self) -> dict | None:
        if self.request:
            if auth_ := self.request.headers.get("Authorization"):
                method, token = auth_.split(" ")
                if method == 'Bearer':
                    if data := auth.decode_jwt(token):
                        return data

    @cached_property
    def producer(self) -> Producer:
        return self.request.app.state.producer

async def get_context() -> Context:
    return Context()

Info = _Info[Context, RootValueType]

#### Auth ####

class IsAuthenticated(BasePermission):
    message = "User is not authenticated."

    def has_permission(self, source, info: Info, **kwargs):
        return info.context.user is not None

#### Queries ####

@strawberry.type
class Query:
    @strawberry.field
    def _unused(self) -> str:
        return "This field is not used."

#### Mutations ####

@strawberry.type
class Mutation:
    @strawberry.field(permission_classes=[IsAuthenticated])
    async def add_product(self, name: str, info: Info) -> None:
        id = str(uuid.uuid1())
        producer = info.context.producer
        producer.produce("products", value=json.dumps({'id': id, 'name': name}))
        producer.flush()

#### API ####

def get_app():
    return GraphQLRouter(strawberry.Schema(query=Query, mutation=Mutation),
                         context_getter=get_context)
