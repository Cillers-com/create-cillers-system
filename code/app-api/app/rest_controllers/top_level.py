from ..rest_base import RestControllerBase, RestEndpoint
from ..auth import is_authenticated, is_admin

class TopLevelController(RestControllerBase):
    root_level = True  # Set this to True to add routes at the root level

    @RestEndpoint("GET", "/hello", auth=is_authenticated)
    async def hello(self):
        user_name = self.context.user.get('name', 'User') if self.context.user else 'User'
        return {"message": f"Welcome to Cillers, {user_name}!"}

    @RestEndpoint("GET", "/hello_admin", auth=is_admin)
    async def hello_admin(self):
        user_name = self.context.user.get('name', 'Admin')
        return {"message": f"Welcome to Cillers, {user_name}! You are an admin."}
