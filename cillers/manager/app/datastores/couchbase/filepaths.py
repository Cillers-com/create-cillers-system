from pathlib import Path
from ... import filepaths

COUCHBASE_APP_ROOT = filepaths.APP_ROOT / Path('datastores/couchbase/')
COUCHBASE_CHANGES_ROOT = filepaths.CHANGES_ROOT / 'couchbase'
STANDARDS = COUCHBASE_APP_ROOT / 'standards.yml'
CONF = filepaths.CONF_ROOT_DATASTORES / 'couchbase.yml'
