from typing import TypeAlias, Optional
from functools import cached_property
from strawberry.fastapi import BaseContext
from strawberry.types.info import RootValueType
from strawberry.types import Info as _Info
from fastapi import Request
from . import jwt

# GraphQL Context
class Context(BaseContext):
    @cached_property
    def user(self) -> Optional[dict]:
        if self.request:
            return get_current_user(self.request)
        return None

# REST Context
class RestContext:
    def __init__(self, request: Request):
        self.request = request
        self._user = None

    @cached_property
    def user(self) -> Optional[dict]:
        if self._user is None:
            self._user = get_current_user(self.request)
        return self._user

def get_current_user(request: Request) -> Optional[dict]:
    if auth_header := request.headers.get("Authorization"):
        scheme, token = auth_header.split()
        if scheme.lower() == 'bearer':
            return jwt.verify_and_decode_jwt(token)
    return None

# For GraphQL
async def get_context() -> Context:
    return Context()

# For REST
def get_rest_context(request: Request) -> RestContext:
    return RestContext(request)

Info: TypeAlias = _Info[Context, RootValueType]
