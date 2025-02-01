import logging
import os
from fastapi import FastAPI
from fastapi.openapi.utils import get_openapi
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from . import init, graphql

logger = logging.getLogger(__name__)
app = FastAPI()

origins = [
    "http://localhost:11000",
    "http://localhost:11001",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.on_event("startup")
async def reinit():
    init.init()

app.include_router(graphql.get_app(), prefix="/api/graphql")

