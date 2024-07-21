from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import logging

from . import graphql, init

logger = logging.getLogger(__name__)

#### Routes ####

app = FastAPI()

origins = [
    "http://localhost:3000"
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

app.include_router(graphql.get_app(), prefix="/api")
