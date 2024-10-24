from fastapi import APIRouter, Depends, HTTPException, Request, status
from pydantic import BaseModel
from src.clients.redpanda import create_event

router = APIRouter()

class MessageResponse(BaseModel):
    message: str

@router.post("/items", response_model=MessageResponse, description="Ingest an item.")
async def item(data: dict) -> MessageResponse:
    create_event('items', data)
    return MessageResponse(message="Item ingested")
