from fastapi import APIRouter, Depends, HTTPException, Request
import logging
import importlib
import pkgutil
from pathlib import Path
from typing import Callable, Any
from .auth import is_authenticated
from .context import RestContext, get_rest_context
from .rest_base import RestControllerBase, RestEndpoint

logger = logging.getLogger(__name__)

# Main router
main_router = APIRouter()

def load_controllers():
    for _, module_name, _ in pkgutil.iter_modules([Path(__file__).parent / "rest_controllers"]):
        module = importlib.import_module(f"app.rest_controllers.{module_name}")
        for attr_name in dir(module):
            attr = getattr(module, attr_name)
            if isinstance(attr, type) and issubclass(attr, RestControllerBase) and attr != RestControllerBase:
                for method_name in dir(attr):
                    method = getattr(attr, method_name)
                    if isinstance(method, RestEndpoint):
                        full_path = f"/{module_name}{method.path}"
                        getattr(main_router, method.method.lower())(full_path)(
                            create_endpoint_handler(attr, method.func, method.auth or is_authenticated)
                        )

def create_endpoint_handler(controller_class, func: Callable, auth_func: Callable):
    async def handler(request: Request):
        context = get_rest_context(request)
        is_authed = await auth_func(context.user)
        if not is_authed:
            raise HTTPException(status_code=403, detail="Not authorized")
        controller = controller_class(context)
        
        # Handle request body for POST and PUT methods
        if request.method in ['POST', 'PUT']:
            body = await request.json()
            return await func(controller, body, **request.path_params)
        else:
            return await func(controller, **request.path_params)
    
    return handler

# Load all controllers
load_controllers()

# Function to get the main router
def get_app():
    return main_router
