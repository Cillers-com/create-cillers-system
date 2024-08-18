from typing import TypeAlias
from functools import cached_property
from strawberry.fastapi import BaseContext
from strawberry.types.info import RootValueType
from strawberry.types import Info as _Info
from . import jwt 

class Context(BaseContext):
    @cached_property
    def user(self) -> dict | None:
        if self.request:
            if auth_ := self.request.headers.get("Authorization"):
                method, token = auth_.split(" ")
                if method == 'Bearer':
                    if data := jwt.verify_and_decode_jwt(token):
                        print(data)
                        return data

async def get_context() -> Context:
    return Context()

Info: TypeAlias = _Info[Context, RootValueType]