import logging
from fastapi import FastAPI
from . import init, graphql, rest

logger = logging.getLogger(__name__)

app = FastAPI()

@app.on_event("startup")
async def reinit():
    init.init()

app.include_router(graphql.get_app(), prefix="/api/graphql")
app.include_router(rest.get_app(), prefix="/api")

