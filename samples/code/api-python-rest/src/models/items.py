from couchbase.exceptions import DocumentNotFoundException
from clients import couchbase as couchbase_client
from data_types.items import Item, ItemData, ItemCreated

keyspace = couchbase_client.get_keyspace('items')

def get_items() -> list[Item]:
    result = keyspace.list()
    print(result)
    return [Item.from_couchbase_row(row) for row in result]

def create_item(data: ItemData) -> ItemCreated:
    result = keyspace.insert(data.model_dump())
    return ItemCreated.from_couchbase_mutation_result(result) 

def delete_item(_id: str) -> int:
    return keyspace.remove(_id)

