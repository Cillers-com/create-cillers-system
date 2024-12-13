from fastapi import APIRouter, Query
from pydantic import BaseModel
from openai import OpenAI
from anthropic import Anthropic
import os
from typing import List, Optional
from clients.footway import FootwayClient, InventoryItem

from utils import http_client, log

logger = log.get_logger(__name__)

router = APIRouter()

openai_client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
anthropic_client = Anthropic(api_key=os.getenv("ANTHROPIC_API_KEY"))

class HelloResponse(BaseModel):
    message: str

class QueryRequest(BaseModel):
    prompt: str

class QueryResponse(BaseModel):
    response: str

class CatFactResponse(BaseModel):
    fact: str

class InventorySearchResponse(BaseModel):
    items: List[InventoryItem]
    total_items: int
    current_page: int
    total_pages: int

@router.get("/hello",
            response_model=HelloResponse,
            description="Returns a greeting message.")
async def hello() -> HelloResponse:
    return HelloResponse(message="Hello from the API!")

@router.post("/test/openai",
             response_model=QueryResponse,
             description="Query OpenAI model")
async def query_openai(request: QueryRequest) -> QueryResponse:
    completion = openai_client.chat.completions.create(
        model="gpt-4o-mini",  # Replace with your desired model
        messages=[
            {"role": "system", "content": "You are a helpful assistant."},
            {"role": "user", "content": request.prompt},
        ]
    )
    return QueryResponse(response=completion.choices[0].message.content)

@router.post("/test/anthropic",
             response_model=QueryResponse,
             description="Query Anthropic model")
async def query_claude(request: QueryRequest) -> QueryResponse:
    messages = [{"role": "user", "content": request.prompt}]

    response = anthropic_client.messages.create(
        system="You are a helpful assistant.",
        model="claude-3-5-haiku-20241022",
        messages=messages,
        max_tokens=300,
        temperature=0.7,
    )
    logger.info(response)
    print(response.content[0].text)
    return QueryResponse(response=response.content[0].text)

@router.get("/test/client",
            response_model=CatFactResponse,
            description="Fetches a random cat fact.")
async def get_cat_fact() -> CatFactResponse:
    with log.level(log.TRACE):
        async with http_client.AsyncClient() as client:
            response = await client.get("https://catfact.ninja/fact")
            response.raise_for_status()
            data = response.json()
    return CatFactResponse(fact=data["fact"])

@router.get("/test/footway",
            response_model=InventorySearchResponse,
            description="Search Footway inventory")
async def search_footway_inventory(
    merchant_id: Optional[List[str]] = Query(None),
    product_name: Optional[str] = None,
    vendor: Optional[List[str]] = Query(None),
    page: int = 1,
    page_size: int = 20
) -> InventorySearchResponse:
    footway_client = FootwayClient(api_key=os.getenv("FOOTWAY_API_KEY"))
    try:
        response = await footway_client.search_inventory(
            merchant_id=merchant_id,
            product_name=product_name,
            vendor=vendor,
            page=page,
            page_size=page_size
        )
        return response
    finally:
        await footway_client.close()
