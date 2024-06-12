import os
import logging

from . import config_file 

logger = logging.getLogger(__name__)

path = '/root/conf/data_stores.yml'

def expand_top_level(initial_parse):
    return initial_parse

def parse():
    initial_parse = config_file.initial_parse(path)
    expanded_top_level = expand_top_level(initial_parse)
    return expanded_top_level

def filter(config, target_data_stores): 
    filtered_top_level = {key: value for key, value in config.items() if key in filter_dict}

    # Further filter each relevant section by its 'clusters', based on filter_dict values
    for key, value in filtered_top_level.items():
        if 'clusters' in value and isinstance(value['clusters'], dict):
            # Keep only clusters whose keys match the strings listed in filter_dict[key]
            value['clusters'] = {k: v for k, v in value['clusters'].items() if k in filter_dict[key]}

    return filtered_top_level
