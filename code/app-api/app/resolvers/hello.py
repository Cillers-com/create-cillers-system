import strawberry
import logging
from .. import types
from ..auth import IsAuthenticated, IsAdmin

logger = logging.getLogger(__name__)

@strawberry.type
class Query:
    @strawberry.field(permission_classes=[IsAuthenticated])
    def hello(self) -> types.Message:
        return types.Message(message="Welcome to Cillers!")

    @strawberry.field(permission_classes=[IsAdmin])
    def hello_admin(self) -> types.Message:
        return types.Message(message="Welcome to Cillers! You are an admin.")

