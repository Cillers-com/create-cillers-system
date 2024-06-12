import os
import logging

from . import config_file 

logger = logging.getLogger(__name__)

path = '/root/conf/change_maker.yml'

def parse():
    environment = os.getenv("ENVIRONMENT")  
    initial_parse = config_file.initial_parse(path)[environment]
    return {key: [value] if isinstance(value, str) else value for key, value in initial_parse.items()}
