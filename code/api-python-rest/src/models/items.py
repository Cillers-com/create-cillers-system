from typing import List
from pydantic import BaseModel

class Item(BaseModel):
    id: int
    name: str

def get_items() -> List[Item]:
    # TODO: Implement actual logic to fetch items from the database
    return [Item(id=1, name="Sample Item")]

def create_item(name: str) -> Item:
    # TODO: Implement actual logic to create an item in the database
    return Item(id=1, name=name)

def delete_item(id: int) -> bool:
    # TODO: Implement actual logic to delete an item from the database
    return True
