from fastapi import APIRouter
from pydantic import BaseModel
from openai import OpenAI
from anthropic import Anthropic
import os

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
