import strawberry
import logging
from .. import types
from ..auth import IsAuthenticated

logger = logging.getLogger(__name__)

@strawberry.type
class Query:
    @strawberry.field(permission_classes=[IsAuthenticated])
    def hello(self) -> types.Message:
        return types.Message(message="Welcome to Cillers!")

