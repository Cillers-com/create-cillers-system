from fastapi import APIRouter, Depends, HTTPException, Request, status
from pydantic import BaseModel
from context import get_rest_context, RestContext
from models import items
from data_types.items import Item, ItemData, ItemCreated

router = APIRouter()

class HelloResponse(BaseModel):
    message: str

class ItemCreateInput(BaseModel):
    name: str

def get_current_user(request: Request, context: RestContext = Depends(get_rest_context)):
    if "Authorization" not in request.headers:
        raise HTTPException(status_code=401, detail="Unauthorized")
    return {"id": "123", "name": "John Doe"}

@router.get("/hello", response_model=HelloResponse, description="Returns a greeting message for the authenticated user.")
async def hello(user: dict = Depends(get_current_user)) -> HelloResponse:
    return HelloResponse(message=f"Hello, {user.get('name', 'User')}!")

@router.get("/items", response_model=list[Item], description="Returns a list of items for the authenticated user.")
async def get_items(user: dict = Depends(get_current_user)) -> list[Item]:
    return items.get_items()

@router.post("/items", response_model=ItemCreated, status_code=status.HTTP_201_CREATED, description="Creates a new item for the authenticated user.")
async def create_item(data: ItemData, user: dict = Depends(get_current_user)) -> ItemCreated:
    return items.create_item(data)

@router.delete("/items/{id}", status_code=status.HTTP_204_NO_CONTENT, description="Deletes a specific item for the authenticated user.")
async def delete_item(id: str, user: dict = Depends(get_current_user)):
    if items.delete_item(id):
        return None
    else:
        raise HTTPException(status_code=404, detail="Item not found")
