from fastapi import APIRouter, HTTPException, Request, Body
import logging
import importlib
import pkgutil
from pathlib import Path
from typing import Type, Dict, Any, get_origin, get_args
from inspect import signature, Parameter
from pydantic import BaseModel
from .auth import is_authenticated
from .context import RestContext, get_rest_context
from .rest_base import RestControllerBase, RestEndpoint

logger = logging.getLogger(__name__)

main_router = APIRouter()

def load_controllers():
    controller_modules = get_controller_modules()
    for module in controller_modules:
        controller_classes = get_controller_classes(module)
        for controller_class in controller_classes:
            register_controller_endpoints(controller_class)

def get_controller_modules():
    controllers_path = Path(__file__).parent / "rest_controllers"
    return [
        importlib.import_module(f"app.rest_controllers.{module_name}")
        for _, module_name, _ in pkgutil.iter_modules([controllers_path])
    ]

def get_controller_classes(module) -> list[Type[RestControllerBase]]:
    return [
        getattr(module, attr_name)
        for attr_name in dir(module)
        if isinstance(getattr(module, attr_name), type)
        and issubclass(getattr(module, attr_name), RestControllerBase)
        and getattr(module, attr_name) != RestControllerBase
    ]

def register_controller_endpoints(controller_class: Type[RestControllerBase]):
    for method_name in dir(controller_class):
        method = getattr(controller_class, method_name)
        if isinstance(method, RestEndpoint):
            endpoint_path = get_endpoint_path(controller_class, method)
            endpoint_handler = create_endpoint_handler(controller_class, method)
            register_endpoint(method.method, endpoint_path, endpoint_handler, method.kwargs)

def get_endpoint_path(controller_class: Type[RestControllerBase], method: RestEndpoint) -> str:
    if controller_class.root_level:
        return method.path
    return f"/{controller_class.__module__.split('.')[-1]}{method.path}"

def create_endpoint_handler(controller_class: Type[RestControllerBase], method: RestEndpoint):
    async def endpoint_handler(request: Request, body: Dict[str, Any] = Body(None)):
        context = get_rest_context(request)
        await authenticate_request(method, context)
        controller = controller_class(context)

        kwargs = {}
        sig = signature(method.func)
        params_param = next((param for name, param in sig.parameters.items() if name == 'params'), None)

        if params_param and params_param.annotation != Parameter.empty:
            params_type = params_param.annotation
            if issubclass(params_type, BaseModel):
                if method.method.upper() in ['POST', 'PUT', 'PATCH']:
                    params = params_type(**body)
                else:
                    params = params_type(**{**dict(request.query_params), **request.path_params})
                kwargs['params'] = params
            else:
                kwargs.update(request.path_params)
                if method.method.upper() not in ['POST', 'PUT', 'PATCH']:
                    kwargs.update(dict(request.query_params))
        else:
            kwargs.update(request.path_params)
            if method.method.upper() not in ['POST', 'PUT', 'PATCH']:
                kwargs.update(dict(request.query_params))

        return await method.func(controller, **kwargs)

    # Update the signature of the endpoint_handler
    sig = signature(method.func)
    return_type = sig.return_annotation
    if get_origin(return_type) is list:
        return_type = get_args(return_type)[0]
    
    parameters = [
        Parameter(name='request', kind=Parameter.POSITIONAL_OR_KEYWORD, annotation=Request),
    ]
    if method.method.upper() in ['POST', 'PUT', 'PATCH']:
        parameters.append(Parameter(name='body', kind=Parameter.POSITIONAL_OR_KEYWORD, annotation=Dict[str, Any], default=Body(None)))
    
    endpoint_handler.__signature__ = sig.replace(parameters=parameters, return_annotation=return_type)

    return endpoint_handler

async def authenticate_request(method: RestEndpoint, context: RestContext):
    auth_func = method.auth if method.auth is not None else is_authenticated
    if not await auth_func(context.user):
        raise HTTPException(status_code=403, detail="Not authorized")

def register_endpoint(method: str, path: str, handler, kwargs: dict):
    getattr(main_router, method.lower())(path, **kwargs)(handler)

# Load all controllers
load_controllers()

# Function to get the main router
def get_app():
    return main_router
