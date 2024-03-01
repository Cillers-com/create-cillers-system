import asyncio
from typing import AsyncGenerator
from functools import cached_property
import strawberry
from strawberry.fastapi import BaseContext, GraphQLRouter
from strawberry.types import Info as _Info
from strawberry.types.info import RootValueType
import logging

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

async def get_context() -> Context:
    return Context()

Info = _Info[Context, RootValueType]

#### Mutations ####

@strawberry.type
class Mutation:
    @strawberry.mutation
    async def set_value(self, value: str) -> str:
        return f"Hello from the mutation stub: got {value}!"

#### Queries ####

@strawberry.type
class Query:
    @strawberry.field
    def hello(self) -> str:
        return "Hello from the query stub!"

#### Subscriptions ####

@strawberry.type
class Subscription:
    @strawberry.subscription
    async def count(self, target: int = 100) -> AsyncGenerator[int, None]:
        for i in range(target):
            yield i
            await asyncio.sleep(0.5)

#### API ####

def get_app():
    return GraphQLRouter(
        strawberry.Schema(Query, mutation=Mutation, subscription=Subscription),
        context_getter=get_context
    )
