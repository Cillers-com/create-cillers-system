from ..rest_base import RestControllerBase, RestEndpoint
from ..auth import is_authenticated
from .. import couchbase as cb, env
import uuid
from fastapi import HTTPException
from fastapi.responses import Response
from pydantic import BaseModel

class ParamsItemCreate(BaseModel):
    name: str

class ParamsItemResponse(BaseModel):
    id: str
    name: str

class ItemsController(RestControllerBase):
    def __init__(self, context):
        super().__init__(context)

    @RestEndpoint("GET", "", auth=is_authenticated)
    async def index(self) -> list[ParamsItemResponse]:
        result = cb.exec(
            env.get_couchbase_conf(),
            f"SELECT name, META().id FROM {env.get_couchbase_bucket()}._default.items"
        )
        return [ParamsItemResponse(id=r['id'], name=r['name']) for r in result]

    @RestEndpoint("POST", "", auth=is_authenticated)
    async def create(self, params: ParamsItemCreate) -> ParamsItemResponse:
        id = str(uuid.uuid1())
        cb.insert(env.get_couchbase_conf(),
                  cb.DocSpec(bucket=env.get_couchbase_bucket(),
                             collection='items',
                             key=id,
                             data={'name': params.name}))
        return ParamsItemResponse(id=id, name=params.name)

    @RestEndpoint("DELETE", "/{id}", auth=is_authenticated)
    async def remove(self, id: str):
        try:
            cb.remove(env.get_couchbase_conf(),
                      cb.DocRef(bucket=env.get_couchbase_bucket(),
                                collection='items',
                                key=id))
            return Response(status_code=204)
        except Exception as e:
            raise HTTPException(status_code=404, detail=f"Item with id {id} not found")
