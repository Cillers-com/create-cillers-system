from typing import AsyncGenerator, List
import strawberry
import uuid
import logging
from .. import couchbase as cb, env
from ..models import items as items_model

logger = logging.getLogger(__name__)

@strawberry.type
class Query:
    @strawberry.field
    def items(self) -> list[items_model.Item]:
        return items_model.list()

@strawberry.type
class Mutation:
    @strawberry.field
    async def items_create(self, items: List[items_model.ItemCreateInput]) -> List[items_model.Item]:
        return items_model.create(items)

    @strawberry.field
    async def items_remove(self, ids: List[str]) -> List[str]:
        return items_model.remove(ids)

@strawberry.type
class Subscription:
    @strawberry.subscription
    async def items(self, info: strawberry.types.Info) -> AsyncGenerator[items_model.ItemsChange, None]:
        async for change in items_model.changes(5, 50):
            yield change 

