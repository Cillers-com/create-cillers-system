from pathlib import Path
from ... import filepaths

COUCHBASE_APP_ROOT = filepaths.APP_ROOT / Path('services/couchbase/')
COUCHBASE_CHANGES_ROOT = filepaths.CHANGES_ROOT / 'couchbase'
STANDARDS = COUCHBASE_APP_ROOT / 'standards.yml'
CONF_ROOT = filepaths.CONF_ROOT_SERVICES / 'couchbase'
CONF = CONF_ROOT / 'cillers.yml'
