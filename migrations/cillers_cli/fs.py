import os
import yaml
import re
import traceback

from . import log
from .types import parse, Migration

logger = log.get_logger(__name__)

def list_yaml_files(path: str) -> list[str]:
    return sorted([os.path.join(path, f) for f in os.listdir(path)
                   if os.path.isfile(os.path.join(path, f))
                   and f.lower().endswith(('.yml', '.yaml'))])

def validate_migration_dir(path, write):
    path = os.path.realpath(os.path.normpath(path))
    if not os.path.isdir(path):
        logger.error(f"{log.cyan(path)} is not a directory.")
        return
    if not os.access(path, os.W_OK if write else os.R_OK):
        logger.error(f"{log.cyan(path)} is not writable.")
        return
    return path

def load_migrations(migrations_dir: str) -> list[Migration]:
    files = sorted(list_yaml_files(migrations_dir))

    migrations = []
    for file in files:
        id = os.path.splitext(os.path.basename(file))[0]
        if re.match(r'^\d{4}-\d{2}-\d{2}-[a-z-0-9_-]+$', id):
            try:
                with open(file) as f:
                    data = yaml.safe_load(f)
                    ops = parse(data)
                    migrations.append(Migration(id=id, ops=ops))
            except Exception:
                logger.error('Failed to load migration %s:\n%s',
                             log.blue(id),
                             log.red(traceback.format_exc()))
        else:
            logger.error(f'Invalid migration id {log.red(id)} (must be '
                         f'on the form {log.blue("YYYY-MM-DD-<id>")}, where '
                         f'{log.blue("<id>")} consists of the characters [a-z-0-9_-].)'
                         ' Skipping...')

    return migrations

def migration_to_yaml(migration: Migration) -> str:
    return yaml.safe_dump(
        migration.model_dump(exclude_none=True, by_alias=True, exclude=['id'])
    )

def write_migration(migrations_dir: str, migration: Migration):
    path = os.path.realpath(
        os.path.normpath(os.path.join(migrations_dir, f'{migration.id}.yaml'))
    )
    if os.path.isfile(path):
        raise FileExistsError(f"There's already a migration file at path {path}")
    with open(path, 'w') as f:
        f.write(migration_to_yaml(migration))
        logger.info(f"Wrote migration {log.blue(migration.id)} to {log.cyan(path)}")
