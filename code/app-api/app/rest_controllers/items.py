from ..rest_base import RestControllerBase, RestEndpoint
from ..auth import is_authenticated, is_admin
from .. import couchbase as cb, env
import uuid
from fastapi import HTTPException

class ItemsController(RestControllerBase):
    @RestEndpoint("GET", "", auth=is_authenticated)
    async def index(self) -> list[dict]:
        result = cb.exec(
            env.get_couchbase_conf(),
            f"SELECT name, META().id FROM {env.get_couchbase_bucket()}._default.items"
        )
        return [{"id": r['id'], "name": r['name']} for r in result]

    @RestEndpoint("POST", "", auth=is_authenticated)
    async def create(self, items: list[dict]) -> list[dict]:
        created_items = []
        for item in items:
            id = str(uuid.uuid1())
            cb.insert(env.get_couchbase_conf(),
                      cb.DocSpec(bucket=env.get_couchbase_bucket(),
                                 collection='items',
                                 key=id,
                                 data={'name': item['name']}))
            created_item = {"id": id, "name": item['name']}
            created_items.append(created_item)
        return created_items

    @RestEndpoint("DELETE", "/{id}", auth=is_authenticated)
    async def remove(self, id: str):
        try:
            cb.remove(env.get_couchbase_conf(),
                      cb.DocRef(bucket=env.get_couchbase_bucket(),
                                collection='items',
                                key=id))
        except Exception as e:
            raise HTTPException(status_code=404, detail=f"Item with id {id} not found")
        return {"message": "Item removed successfully"}
