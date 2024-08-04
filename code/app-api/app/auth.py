from strawberry.permission import BasePermission
from .context import Info

class IsAuthenticated(BasePermission):
    message = "User is not authenticated."
    error_extensions = {"code": "UNAUTHORIZED"}

    def has_permission(self, source, info: Info, **kwargs):
        return info.context.user is not None