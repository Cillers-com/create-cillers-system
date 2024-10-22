import logging
import os
from fastapi import FastAPI
from fastapi.openapi.utils import get_openapi
from fastapi.responses import JSONResponse
from . import init, graphql, rest

logger = logging.getLogger(__name__)
app = FastAPI()

def generate_openapi_schema():
    """
    Generate the OpenAPI schema for the FastAPI application, excluding the GraphQL API.
    """
    routes_to_include = [
        route for route in app.routes 
        if not route.path.startswith("/api/graphql")
    ]

    openapi_schema = get_openapi(
        title="My API",
        version="1.0.0",
        description="This is my API description",
        routes=routes_to_include,  # Use the filtered routes
    )
    
    # Use environment variable for server URL, with a default fallback
    server_url = os.getenv("APP_PROTOCOL_HOST_PORT")
    
    openapi_schema["servers"] = [
        {"url": server_url, "description": "API server"}
    ]
    
    app.openapi_schema = openapi_schema
    return app.openapi_schema

@app.on_event("startup")
async def reinit():
    init.init()

app.include_router(graphql.get_app(), prefix="/api/graphql")
app.include_router(rest.get_app(), prefix="/api")

@app.get("/api/openapi.json")
def get_openapi_endpoint():
    """
    Retrieve the generated OpenAPI schema.
    """
    return JSONResponse(content=generate_openapi_schema())
