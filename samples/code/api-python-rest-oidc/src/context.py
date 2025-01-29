from typing import Optional
from functools import cached_property
from fastapi import Request
import jwt_utils

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
            return jwt_utils.verify_and_decode_jwt(token)
    return None

# For REST
def get_rest_context(request: Request) -> RestContext:
    return RestContext(request)
