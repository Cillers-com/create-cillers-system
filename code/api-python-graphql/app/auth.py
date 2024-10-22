from strawberry.permission import BasePermission
from .context import get_current_user, Info

async def is_authenticated(current_user: dict) -> bool:
    return current_user is not None

async def is_admin(current_user: dict) -> bool:
    return current_user is not None and 'admin' in current_user.get('roles', [])

# GraphQL specific permissions
class IsAuthenticated(BasePermission):
    message = "User is not authenticated."
    error_extensions = {"code": "UNAUTHORIZED"}

    def has_permission(self, source, info: Info, **kwargs):
        return info.context.user is not None

class IsAdmin(BasePermission):
    message = "User is not admin."
    error_extensions = {"code": "UNAUTHORIZED"}

    def has_permission(self, source, info: Info, **kwargs):
        user = info.context.user
        return user is not None and 'admin' in user.get('roles', [])
