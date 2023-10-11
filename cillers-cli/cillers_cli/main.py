import argparse
import sys
import traceback

import rich.traceback

from . import env, fs, log, couchbase, create_resource

logger = log.get_logger(__name__)

def handle_create_resource(args):
    if not env.validate():
        logger.error("Environment variables are not set correctly – aborting.")
        return 1
    configs = env.get_configs()
    spec = create_resource.ResourceSpec(name=args.name,
                                        bucket=args.bucket,
                                        sink_url=args.sink_url)
    create_resource.create(configs, spec, args.migration_dir)

def handle_apply_migrations(args) -> bool:
    if not env.validate():
        logger.error("Environment variables are not set correctly – aborting.")
        return 1
    migrations = fs.load_migrations(args.migration_dir)
    configs = env.get_configs()
    cb_conf = configs.couchbase
    applied_ids = set(m.get('id')
                      for m in couchbase.list_recorded(cb_conf)
                      if 'id' in m)
    to_apply = [m for m in migrations if m.id not in applied_ids]
    if to_apply:
        n = len(to_apply)
        logger.info(f"Applying {log.cyan(str(n))} migrations...")
        for migration in to_apply:
            try:
                logger.info(f"Applying migration {log.blue(migration.id)}.")
                for i, op in enumerate(migration.ops):
                    try:
                        op.apply(configs)
                    except Exception:
                        logger.error(
                            "Failed to apply operation %s in migration %s:\n%s",
                            log.red(str(i)),
                            log.blue(migration.id),
                            log.red(traceback.format_exc())
                        )
                        raise
                couchbase.record(cb_conf, migration.id)
                logger.info(f"Migration {log.blue(migration.id)} applied successfully.")
            except Exception:
                logger.error("Failed to apply migration %s:\n%s",
                             log.blue(migration.id),
                             log.red(traceback.format_exc()))

                return 1
        logger.info(f"Successfully applied {log.cyan(str(n))} migrations.")
    else:
        n = len(migrations)
        logger.info("No migrations to apply (%s migrations already applied).",
                    log.cyan(str(n)))
    return 0

def parse_args(args: list[str]):
    rich.traceback.install(show_locals=True)
    parser = argparse.ArgumentParser(description="The Cillers CLI")
    subparsers = parser.add_subparsers()

    migrate_parser = subparsers.add_parser('migrate',
                                           help='Apply all pending migrations')
    migrate_parser.add_argument('--migration-dir',
                                default='migrations',
                                help='The migration directory.')
    migrate_parser.set_defaults(command=handle_apply_migrations)

    create_parser = subparsers.add_parser('create-resource',
                                          help='Create a new resource type')
    create_parser.add_argument('name', help='Name of the resource')
    create_parser.add_argument('--bucket',
                               default='_default',
                               help='The bucket to use for the resource.')
    create_parser.add_argument('--sink-url',
                               help='Optional HTTP sink URL.')
    create_parser.add_argument('--migration-dir',
                               default='migrations',
                               help='The migration directory.')
    create_parser.set_defaults(command=handle_create_resource)

    args = parser.parse_args(args)

    if not args.command:
        parser.print_help()
        parser.exit(status=1, message="\nError: No subcommand specified.\n")

    return args

def main(args: list[str]) -> int:
    parsed_args = parse_args(args)
    result = parsed_args.command(parsed_args)
    if isinstance(result, int):
        return result
    return 0

if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
