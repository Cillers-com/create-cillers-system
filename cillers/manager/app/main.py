import sys
import logging
import rich
from .config_cillers import ConfigCillers
from .datastores import get_controller

logger = logging.getLogger(__name__)
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)

rich.traceback.install(show_locals=True)

conf = ConfigCillers()

def change():
    for datastore_id in conf.datastores:
        get_controller(datastore_id).change()
    sys.exit(0)

def validate_config():
    raise NotImplementedError

