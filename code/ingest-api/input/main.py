import argparse
import sys
import logging

from . import init, http_server, env

logger = logging.getLogger(__name__)

def handle_run(args):
    """Runs the server."""
    if v := init.init():
        return v
    http_server.run(env.get_http_conf(), "input.routes:app")

def parse_args(args: list[str]):
    """Parses command-line arguments."""
    parser = argparse.ArgumentParser(description="Example app.")
    subparsers = parser.add_subparsers()

    run_parser = subparsers.add_parser('run')
    run_parser.set_defaults(command=handle_run)

    args = parser.parse_args(args)

    if 'command' not in args:
        parser.print_help()
        parser.exit(status=1, message="\nError: No subcommand specified.\n")

    return args

def run(args: list[str] = []) -> int:
    """Runs the application."""
    parsed_args = parse_args(args)
    result = parsed_args.command(parsed_args)
    if isinstance(result, int):
        return result
    return 0

def main():
    """Main entry point."""
    sys.exit(run(sys.argv[1:]))
