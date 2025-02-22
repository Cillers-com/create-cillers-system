import os
import uvicorn
from fastapi import FastAPI, Depends, APIRouter
from fastapi.openapi.utils import get_openapi
from fastapi.middleware.cors import CORSMiddleware
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
        {"url": api_url_for_apps, "description": "API"}
        ]
)
app.include_router(router, prefix="/api")

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

def custom_openapi():
    if app.openapi_schema:
        return app.openapi_schema
    openapi_schema = get_openapi(
        title="Your API Title",
        version="1.0.0",
        description="Your API Description",
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
