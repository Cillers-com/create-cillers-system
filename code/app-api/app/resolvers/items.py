import asyncio
import time
from typing import AsyncGenerator, List
import strawberry
import uuid
import logging
from .. import couchbase as cb, env
from ..auth import IsAuthenticated

logger = logging.getLogger(__name__)

def list_items():
    result = cb.exec(
        env.get_couchbase_conf(),
        f"SELECT name, META().id FROM {env.get_couchbase_bucket()}._default.items"
    )
    return [Item(**r) for r in result]

@strawberry.type
class Item:
    id: str
    name: str

@strawberry.input
class ItemCreateInput:
    name: str

@strawberry.type
class Query:
    @strawberry.field
    def items(self) -> list[Item]:
        return list_items()

@strawberry.type
class Mutation:
    @strawberry.field(permission_classes=[IsAuthenticated])
    async def items_create(self, items: List[ItemCreateInput]) -> List[Item]:
        created_items = []
        for item in items:
            id = str(uuid.uuid1())
            cb.insert(env.get_couchbase_conf(),
                      cb.DocSpec(bucket=env.get_couchbase_bucket(),
                                 collection='items',
                                 key=id,
                                 data={'name': item.name}))
            created_item = Item(id=id, name=item.name)
            created_items.append(created_item)
        return created_items

    @strawberry.field(permission_classes=[IsAuthenticated])
    async def items_remove(self, ids: List[str]) -> List[str]:
        for id in ids:
            cb.remove(env.get_couchbase_conf(),
                      cb.DocRef(bucket=env.get_couchbase_bucket(),
                                collection='items',
                                key=id))
        return ids

@strawberry.type
class Subscription:
    @strawberry.subscription(permission_classes=[IsAuthenticated])
    async def items_created(self, info: strawberry.types.Info) -> AsyncGenerator[Item, None]:
        seen = set(p.id for p in list_items())
        while True:
            current_time = int(time.time())
            for p in list_items():
                if p.id not in seen:
                    seen.add(p.id)
                    yield p
            await asyncio.sleep(0.5)
