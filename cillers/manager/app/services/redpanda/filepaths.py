from pathlib import Path
from ... import filepaths

REDPANDA_APP_ROOT = filepaths.APP_ROOT / Path('datastores/redpanda/')
REDPANDA_CHANGES_ROOT = filepaths.CHANGES_ROOT / 'redpanda'
STANDARDS = REDPANDA_APP_ROOT / 'standards.yml'
CONF = filepaths.CONF_ROOT_DATASTORES / 'redpanda.yml'
