from pydantic import BaseModel
import logging
from couchbase.result import MutationResult

class ItemData(BaseModel):
    name: str
    
    @classmethod
    def from_dict(cls, data: dict):
        return cls(**data)

class Item(BaseModel):
    id: str
    data: ItemData
    
    @classmethod
    def from_couchbase_row(cls, row: dict) -> 'Item':
        logging.debug(row)
        return cls(
            id=row['id'],
            data=row['items']
        )

class ItemCreated(BaseModel):
    id: str
    cas: int 
    
    @classmethod
    def from_couchbase_mutation_result(cls, result: MutationResult) -> 'ItemCreated':
        return cls(
            id=result.key,
            cas=result.cas
        )


