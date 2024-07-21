import asyncio
import time
import logging
from typing import List, Optional
import strawberry
import uuid
from .. import couchbase as cb, env

logger = logging.getLogger(__name__)

@strawberry.type
class Item:
    id: str
    name: str

@strawberry.type
class ItemsChange:
    existing: Optional[List[Item]] = None
    created: Optional[List[Item]] = None
    removed: Optional[List[str]] = None
    updated: Optional[List[Item]] = None

@strawberry.input
class ItemCreateInput:
    name: str

def list():
    result = cb.exec(
        env.get_couchbase_conf(),
        f"SELECT name, META().id FROM {env.get_couchbase_bucket()}._default.items"
    )
    return [Item(**r) for r in result]

def create(items):
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

def remove(ids):
    for id in ids:
        cb.remove(env.get_couchbase_conf(),
                  cb.DocRef(bucket=env.get_couchbase_bucket(),
                            collection='items',
                            key=id))
    return ids

async def changes(initial_batch_size, subsequent_batch_size):
    seen = set()
    batch = []
    has_sent_first_batch = False
    existing_items = list()
    index = 0
    end = 0
    while end < len(existing_items):
        start = end
        end = initial_batch_size + index * subsequent_batch_size
        index += 1
        batch = existing_items[start:end]
        yield ItemsChange(existing=batch)
        for item in batch:
            seen.add(item.id)
    while True:
        items = list()
        new_items = []
        for item in items:
            if item.id not in seen:
                new_items.append(item)
                seen.add(item.id)
        index = 0 
        end = 0
        while end < len(new_items):
            start = end 
            end = initial_batch_size + index * subsequent_batch_size
            index += 1
            batch = new_items[start:end]
            yield ItemsChange(created=batch)
        await asyncio.sleep(0.5)


