import strawberry
from strawberry.tools import merge_types
from strawberry.fastapi import GraphQLRouter
import logging
import importlib
import pkgutil
from pathlib import Path
from .context import get_context

logger = logging.getLogger(__name__)

resolvers_path = Path(__file__).parent / "resolvers"

classes = {
    'Query': [],
    'Mutation': [], 
    'Subscription': [] 
}

for _, module_name, _ in pkgutil.iter_modules([resolvers_path]):
    module = importlib.import_module(f"app.resolvers.{module_name}")
    for attr_name in dir(module):
        attr = getattr(module, attr_name)
        if isinstance(attr, strawberry.types.types.Type) and attr_name in classes.keys():
            classes[attr_name].append(attr)

Query = merge_types("Query", tuple(classes['Query']))
Mutation = merge_types("Mutation", tuple(classes['Mutation']))
Subscription = merge_types("Subscription", tuple(classes['Subscription']))

def get_app():
    return GraphQLRouter(
        strawberry.Schema(Query, mutation=Mutation, subscription=Subscription),
        context_getter=get_context
    )
