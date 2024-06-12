import argparse
import sys
import logging
import os
from datetime import timedelta
import time
import json
from couchbase.auth import PasswordAuthenticator
from couchbase.cluster import Cluster
from couchbase.diagnostics import ServiceType
from couchbase.options import WaitUntilReadyOptions, ClusterOptions, QueryOptions

from . import init, env, config_file, change_maker_config, clients_config, data_stores_config

logger = logging.getLogger(__name__)

def get_nested_value(data_dict, key_string):
    keys = key_string.split('.')
    current_data = data_dict
    for key in keys:
        try:
            current_data = current_data[key]
        except KeyError:
            # Key does not exist in the dictionary
            return None
    return current_data

def map_keys_to_values(key_strings, nested_dict):
    return {key_string: get_nested_value(nested_dict, key_string) for key_string in key_strings}

def filter_config(config, filter_dict):
    # Filter top-level keys
    filtered_top_level = {key: value for key, value in config.items() if key in filter_dict}

    # Further filter each relevant section by its 'clusters', based on filter_dict values
    for key, value in filtered_top_level.items():
        if 'clusters' in value and isinstance(value['clusters'], dict):
            # Keep only clusters whose keys match the strings listed in filter_dict[key]
            value['clusters'] = {k: v for k, v in value['clusters'].items() if k in filter_dict[key]}

    return filtered_top_level

def handle_run(args):
    environment = os.getenv("ENVIRONMENT")  
   
    config = { 
        "change_maker": change_maker_config.parse(),
        "data_stores": data_stores_config.parse(),
        "clients": clients_config.parse()
    } 

    print(f"Config: {json.dumps(config)}\n\n")

    for data_store, clusters in config["change_maker"].items():
        data_store_client_configs = clients.get(data_store, {})
        relevant_configs[data_store] = {
            cluster: data_store_client_configs.get(cluster, {}) for cluster in clusters if cluster in data_store_client_configs
        }
        print(data_store_client_configs)

    auth = PasswordAuthenticator('admin', 'password')
    max_retries = 5
    attempt = 0
    while attempt < max_retries:
        try:
            cluster = Cluster.connect('couchbase://couchbase', ClusterOptions(auth))
            cluster.wait_until_ready(timedelta(seconds=10),
                     WaitUntilReadyOptions(service_types=[ServiceType.Management, ServiceType.KeyValue, ServiceType.Query]))
            cluster.wait_until_ready(timedelta(seconds=10))
            print("Couchbase is ready to receive instructions.")
            break
        except Exception as e:
            if attempt < max_retries - 1:
                print("Retrying...")
                time.sleep(2)  # wait for 2 seconds before retrying
            attempt += 1
    return 0
    #if v := init.init():
    #    return v

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
