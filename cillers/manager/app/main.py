import sys
import logging
import rich
from .config_cillers import ConfigCillers
from .services import get_controller_datastore

logger = logging.getLogger(__name__)
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)

rich.traceback.install(show_locals=True)

conf = ConfigCillers()

def provision():
    for service_id in conf.services:
        get_controller(service_id).provision()

def upgrade_data_structures():
    for datastore_id in conf.datastores:
        get_controller_datastore(datastore_id).upgrade_data_structue()
    sys.exit(0)

def validate_config():
    raise NotImplementedError

