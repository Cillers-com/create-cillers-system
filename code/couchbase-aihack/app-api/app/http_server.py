from typing import Annotated
from pydantic import BaseModel, Field
import logging
import uvicorn

logger = logging.getLogger(__name__)

class ServerConf(BaseModel):
    port: Annotated[int, Field(gt=0, le=65535)]
    host: str
    debug: bool = False
    autoreload: bool = False

#### Actions ####

def run(conf: ServerConf, app_ref: str):
    """Runs the server."""
    logger.info(f"Starting server on {conf.host}:{conf.port}")
    uvicorn.run(app_ref,
                host=conf.host,
                port=conf.port,
                log_level="debug" if conf.debug else "info",
                reload=conf.autoreload)
