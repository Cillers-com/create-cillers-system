from fastapi import APIRouter, Depends, HTTPException, Request
from pydantic import BaseModel
from src.context import get_rest_context, RestContext

router = APIRouter()

class HelloResponse(BaseModel):
    message: str

class Item(BaseModel):
    id: int
    name: str

class ItemResponse(BaseModel):
    items: list[Item]

class MessageResponse(BaseModel):
    message: str

def get_current_user(request: Request, context: RestContext = Depends(get_rest_context)):
    if "Authorization" not in request.headers:
        raise HTTPException(status_code=401, detail="Unauthorized")
    print(context.user)
    return {"id": "123", "name": "John Doe"}

@router.get("/hello", response_model=HelloResponse, description="Returns a greeting message for the authenticated user.")
async def hello(user: dict = Depends(get_current_user)) -> HelloResponse:
    return HelloResponse(message=f"Hello, {user.get('name', 'User')}!")

@router.get("/items", response_model=ItemResponse, description="Returns a list of items for the authenticated user.")
async def get_items(user: dict = Depends(get_current_user)) -> ItemResponse:
    return ItemResponse(items=[Item(id=1, name="Sample Item")])

@router.post("/items", response_model=MessageResponse, description="Creates a new item for the authenticated user.")
async def create_item(item: Item, user: dict = Depends(get_current_user)) -> MessageResponse:
    return MessageResponse(message=f"Item '{item.name}' created successfully")

@router.delete("/items/{id}", response_model=MessageResponse, description="Deletes a specific item for the authenticated user.")
async def delete_item(id: str, user: dict = Depends(get_current_user)) -> MessageResponse:
    return MessageResponse(message=f"Item with id {id} deleted successfully")
