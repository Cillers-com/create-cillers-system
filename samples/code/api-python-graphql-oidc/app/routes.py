import logging
import os
from fastapi import FastAPI
from fastapi.openapi.utils import get_openapi
from fastapi.responses import JSONResponse
from . import init, graphql

logger = logging.getLogger(__name__)
app = FastAPI()

@app.on_event("startup")
async def reinit():
    init.init()

app.include_router(graphql.get_app(), prefix="/api/graphql")

