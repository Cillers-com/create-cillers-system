import rich.traceback
import logging

from . import env

logger = logging.getLogger(__name__)

def init():
    """Initializes the application."""
    rich.traceback.install(show_locals=True)
    if not env.validate():
        logger.error("Environment variables are not set correctly – aborting.")
        return 1
