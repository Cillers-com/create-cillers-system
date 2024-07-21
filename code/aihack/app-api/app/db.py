import uuid
import strawberry
from . import couchbase as cb, env

@strawberry.type
class Item:
    id: str
    name: str

def create_item(name: str) -> Item:
    id = str(uuid.uuid1())
    cb.insert(env.get_couchbase_conf(),
              cb.DocSpec(bucket=env.get_couchbase_bucket(),
                         collection='items',
                         key=id,
                         data={'name': name}))
    return Item(id=id, name=name)
#
def get_item(id: str) -> Item | None:
    if doc := cb.get(env.get_couchbase_conf(),
                     cb.DocRef(bucket=env.get_couchbase_bucket(),
                               collection='items',
                               key=id)):
        return Item(id=id, name=doc['name'])

def delete_item(id: str) -> None:
    cb.remove(env.get_couchbase_conf(),
              cb.DocRef(bucket=env.get_couchbase_bucket(),
                        collection='items',
                        key=id))

def list_items() -> list[Item]:
    result = cb.exec(
        env.get_couchbase_conf(),
        f"SELECT name, META().id FROM {env.get_couchbase_bucket()}._default.items"
    )
    return [Item(**r) for r in result]
