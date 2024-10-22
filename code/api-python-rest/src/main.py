import os
import uvicorn
from fastapi import FastAPI, Depends, APIRouter
from fastapi.openapi.utils import get_openapi
from context import get_rest_context, RestContext
from routes import router
import sys

# Environment variable validation
api_url_for_apps = os.getenv("API_URL_FOR_APPS")
if not api_url_for_apps:
    raise ValueError("API_URL_FOR_APPS environment variable is not set")

api_port = os.getenv("API_PORT")
if not api_port:
    raise ValueError("API_PORT environment variable is not set")

api_reload = os.getenv("API_RELOAD", "False").lower() == "true"

app = FastAPI(
    openapi_url="/api/openapi.json",
    docs_url="/api/docs",
    title="Your API Title",
    description="Your API Description",
    version="1.0.0",
    servers=[
        {"url": api_url_for_apps, "description": "API Gateway"}
    ]
)
app.include_router(router, prefix="/api")

def custom_openapi():
    if app.openapi_schema:
        return app.openapi_schema
    openapi_schema = get_openapi(
        title="Your API Title",
        version="1.0.0",
        description="Your API Description. Authentication is handled via a same-site strict cookie that is converted to a JWT Authorization header in the API gateway.",
        routes=app.routes,
    )
    # Ensure the servers information is retained
    openapi_schema["servers"] = [{"url": api_url_for_apps, "description": "API Gateway"}]
    
    # Remove the security schemes and global security requirement
    if "components" in openapi_schema:
        openapi_schema["components"].pop("securitySchemes", None)
    openapi_schema.pop("security", None)
    
    # Remove security requirements from all endpoints
    for path in openapi_schema["paths"].values():
        for operation in path.values():
            operation.pop("security", None)
    
    app.openapi_schema = openapi_schema
    return app.openapi_schema

app.openapi = custom_openapi

def main():
    uvicorn.run(
        "src.main:app",
        host="0.0.0.0",
        port=int(api_port),
        reload=api_reload,
    )

if __name__ == "__main__":
    main()
