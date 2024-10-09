from typing import Callable
from .context import RestContext

class RestControllerBase:
    def __init__(self, context: RestContext):
        self.context = context

class RestEndpoint:
    def __init__(self, method: str, path: str = "", auth: Callable = None):
        self.method = method
        self.path = path
        self.auth = auth
        self.func = None

    def __call__(self, func):
        self.func = func
        return self

    def __get__(self, obj, objtype=None):
        if obj is None:
            return self
        return self.func.__get__(obj, objtype)
