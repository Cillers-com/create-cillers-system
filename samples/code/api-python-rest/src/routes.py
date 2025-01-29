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

@router.get("/hello", response_model=HelloResponse, description="Returns a greeting message.")
async def hello() -> HelloResponse:
    return HelloResponse(message=f"Hello and welcome to Cillers!")

@router.get("/items", response_model=list[Item], description="Returns a list of items.")
async def get_items() -> list[Item]:
    return items.get_items()

@router.post("/items", response_model=ItemCreated, status_code=status.HTTP_201_CREATED, description="Creates a new item.")
async def create_item(data: ItemData) -> ItemCreated:
    return items.create_item(data)

@router.delete("/items/{id}", status_code=status.HTTP_204_NO_CONTENT, description="Deletes a specific item.")
async def delete_item(id: str):
    if items.delete_item(id):
        return None
    else:
        raise HTTPException(status_code=404, detail="Item not found")

