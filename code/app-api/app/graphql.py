import asyncio
import time
from typing import AsyncGenerator
from functools import cached_property
from typing import Dict
import strawberry
from strawberry.fastapi import BaseContext, GraphQLRouter
from strawberry.permission import BasePermission
from strawberry.exceptions import StrawberryGraphQLError
from strawberry.types import Info as _Info
from strawberry.types.info import RootValueType
import logging

from . import auth, db

logger = logging.getLogger(__name__)

#### Context ####

class Context(BaseContext):
    @cached_property
    def user(self) -> dict | None:
        if self.request:
            if auth_ := self.request.headers.get("Authorization"):
                method, token = auth_.split(" ")
                if method == 'Bearer':
                    if data := auth.verify_and_decode_jwt(token):
                        return data

async def get_context() -> Context:
    return Context()

Info = _Info[Context, RootValueType]

#### Auth ####

class IsAuthenticated(BasePermission):
    message = "User is not authenticated."
    error_extensions = {"code": "UNAUTHORIZED"}

    def has_permission(self, source, info: Info, **kwargs):
        return info.context.user is not None

@strawberry.type
class Message:
    message: str

#### Mutations ####

@strawberry.type
class Mutation:
    @strawberry.field(permission_classes=[IsAuthenticated])
    async def add_product(self, name: str) -> db.Product:
        return db.create_product(name)

    @strawberry.field(permission_classes=[IsAuthenticated])
    async def remove_product(self, id: str) -> None:
        db.delete_product(id)

#### Queries ####

@strawberry.type
class Query:
    @strawberry.field
    def products(self) -> list[db.Product]:
        return db.list_products()

    @strawberry.field(permission_classes=[IsAuthenticated])
    def hello(self) -> Message:
        return Message(message="Hej, hej")

#### Subscriptions ####

@strawberry.type
class Subscription:
    @strawberry.subscription(permission_classes=[IsAuthenticated])
    async def product_added(self, info: strawberry.types.Info) -> AsyncGenerator[db.Product, None]:
        seen = set(p.id for p in db.list_products())
        while True:
            current_time = int(time.time())
            if current_time > info.context.user['exp']:
                print("Token has expired")
                await info.context.request.close(code=4403, reason="token_expired")
                break
            
            for p in db.list_products():
                if p.id not in seen:
                    seen.add(p.id)
                    yield p
            await asyncio.sleep(0.5)

#### API ####

def get_app():
    return GraphQLRouter(
        strawberry.Schema(Query, mutation=Mutation, subscription=Subscription),
        context_getter=get_context
    )
