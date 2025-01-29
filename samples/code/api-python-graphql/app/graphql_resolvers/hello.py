import strawberry
import logging
from .. import types

logger = logging.getLogger(__name__)

@strawberry.type
class Query:
    @strawberry.field
    def hello(self) -> types.Message:
        return types.Message(message="Welcome to Cillers!")

