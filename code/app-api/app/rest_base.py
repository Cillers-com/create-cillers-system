from typing import Callable, Optional
from inspect import signature, Parameter

class RestControllerBase:
    root_level: bool = False

    def __init__(self, context):
        self.context = context

class RestEndpoint:
    def __init__(self, method: str, path: str = "", auth: Optional[Callable] = None, **kwargs):
        self.method = method
        self.path = path
        self.auth = auth
        self.func = None
        self.kwargs = kwargs

    def __call__(self, func):
        self.func = func
        return self

    def __get__(self, obj, objtype=None):
        if obj is None:
            return self
        return self.func.__get__(obj, objtype)

    def get_endpoint_parameters(self):
        sig = signature(self.func)
        params = []
        for name, param in sig.parameters.items():
            if name not in ['self', 'context']:
                params.append({
                    'name': name,
                    'type': param.annotation if param.annotation != Parameter.empty else Any,
                    'default': param.default if param.default != Parameter.empty else ...,
                })
        return params
