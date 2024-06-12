import os
import logging

from . import config_file 

logger = logging.getLogger(__name__)

path = '/root/conf/clients.yml'

standards = {
    'couchbase': {
        'standard_local_and_capella': {
            'couchbase': {
                'production': 'standard_production_capella',
                'stage': 'standard_stage_capella',
                'development': 'standard_development_local',
                'test': 'standard_test_local'
            }
        },
        'standard_production_capella': {
                'connection': 'standard_production_connnection_capella',
                'credentials': 'standard_production_credentials'
            },
        'standard_stage_capella': {
                'connection': 'standard_stage_connection_capella',
                'credentials': 'standard_stage_credentials'
            },
        'standard_development_local': {
                'connection': 'standard_development_connection_local',
                'credentials': 'standard_development_credentials'
            },
        'standard_test_local': {
                'connection': 'standard_test_connection_local',
                'credentials': 'standard_test_credentials'
            },
        'standard_production_connection_capella': {
                'protocol': 'couchbases',
                'host': os.getenv('COUCHBASE_PRODUCTION_HOST'),
                'port': 18091
            },
        'standard_stage_connection_capella': {
                'protocol': 'couchbases',
                'host': os.getenv('COUCHBASE_STAGE_HOST'),
                'port': 18091
            },
        'standard_development_connection_local': {
                'protocol': 'couchbase',
                'host': os.getenv('COUCHBASE_DEVELOPMENT_HOST'),
                'port': 8091
            },
        'standard_test_connection_local': {
                'protocol': 'couchbase',
                'host': os.getenv('COUCHBASE_TEST_HOST'),
                'port': 8092
            },
        'standard_production_credentials': {
                'api': {
                        'type': 'basic',
                        'username': os.getenv('COUCHBASE_PRODUCTION_API_USERNAME'),
                        'password': os.getenv('COUCHBASE_PRODUCTION_API_PASSWORD')
                    }, 
                'change_maker': {
                        'type': 'basic',
                        'username': os.getenv('COUCHBASE_PRODUCTION_CHANGE_MAKER_USERNAME'),
                        'password': os.getenv('COUCHBASE_PRODUCTION_CHANGE_MAKER_PASSWORD')
                    }
            },
        'standard_stage_credentials': {
                'api': {
                        'type': 'basic',
                        'username': os.getenv('COUCHBASE_STAGE_API_USERNAME'),
                        'password': os.getenv('COUCHBASE_STAGE_API_PASSWORD')
                    }, 
                'change_maker': {
                        'type': 'basic',
                        'username': os.getenv('COUCHBASE_STAGE_CHANGE_MAKER_USERNAME'),
                        'password': os.getenv('COUCHBASE_STAGE_CHANGE_MAKER_PASSWORD')
                    }
            },
        'standard_development_credentials': {
                'admin': {
                        'type': 'basic',
                        'username': os.getenv('COUCHBASE_DEVELOPMENT_ADMIN_USERNAME'),
                        'password': os.getenv('COUCHBASE_DEVELOPMENT_ADMIN_PASSWORD')
                    } 
            },
        'standard_test_credentials': {
                'admin': {
                        'type': 'basic',
                        'username': os.getenv('COUCHBASE_TEST_ADMIN_USERNAME'),
                        'password': os.getenv('COUCHBASE_TEST_ADMIN_PASSWORD')
                    } 
            },
    },
    'redpanda': {
        'standard_local_and_cloud': {
            'redpanda': {
                'production': 'standard_production_cloud',
                'stage': 'standard_stage_cloud',
                'development': 'standard_redpan_development_local',
                'test': 'standard_test_local'
            }
        },
        'standard_production_cloud': {
                'connection': 'standard_production_connection_cloud',
                'credentials': 'standard_production_credentials'
            },
        'standard_stage_cloud': {
                'connection': 'standard_stage_connection_cloud',
                'credentials': 'standard_stage_credentials'
            },
        'standard_development_local': {
                'connection': 'standard_development_connection_local',
                'credentials': 'standard_development_credentials'
            },
        'standard_test_local': {
                'connection': 'standard_test_connection_local',
                'credentials': 'standard_test_credentials'
            },
        'standard_production_connection_cloud': {
                'host': os.getenv('REDPANDA_PRODUCTION_HOST'),
                'port': 19092
            },
        'standard_stage_connection_cloud': {
                'host': os.getenv('REDPANDA_STAGE_HOST'),
                'port': 19092
            },
        'standard_development_connection_local': {
                'host': 'redpanda',
                'port': 9092
            },
        'standard_test_connection_local': {
                'host': 'redpanda',
                'port': 9092
            },
        'standard_production_credentials': {
                'api': {
                        'type': 'api_key',
                        'username': os.getenv('REDPANDA_PRODUCTION_API_USERNAME'),
                        'password': os.getenv('REDPANDA_PRODUCTION_API_PASSWORD')
                    }, 
                'change_maker': {
                        'type': 'api_key',
                        'username': os.getenv('REDPANDA_PRODUCTION_CHANGE_MAKER_USERNAME'),
                        'password': os.getenv('REDPANDA_PRODUCTION_CHANGE_MAKER_PASSWORD')
                    }
            },
        'standard_stage_credentials': {
                'api': {
                        'type': 'api_key',
                        'username': os.getenv('REDPANDA_STAGE_API_USERNAME'),
                        'password': os.getenv('REDPANDA_STAGE_API_PASSWORD')
                    }, 
                'change_maker': {
                        'type': 'api_key',
                        'username': os.getenv('REDPANDA_STAGE_CHANGE_MAKER_USERNAME'),
                        'password': os.getenv('REDPANDA_STAGE_CHANGE_MAKER_PASSWORD')
                    }
            },
        'standard_development_credentials': {
                'admin': {
                        'type': 'api_key',
                        'username': os.getenv('REDPANDA_DEVELOPMENT_ADMIN_USERNAME'),
                        'password': os.getenv('REDPANDA_DEVELOPMENT_ADMIN_PASSWORD')
                    } 
            },
        'standard_test_credentials': {
                'admin': {
                        'type': 'api_key',
                        'username': os.getenv('REDPANDA_TEST_ADMIN_USERNAME'),
                        'password': os.getenv('REDPANDA_TEST_ADMIN_PASSWORD')
                    } 
            }
    }
}

def replace_standards(config, type):
    if type not in standards:
        raise ValueError(f"'{type}' is not a valid top-level key in the standards dictionary.")
    
    if isinstance(config, dict):
        return {key: replace_standards(value, type) for key, value in config.items()}
    elif isinstance(config, list):
        return [replace_standards(item, type) for item in config]
    elif isinstance(config, str):
        if config.startswith('standard'):
            if config not in standards[type]:
                raise ValueError(f"The configuration '{config}' is not defined in standards[type].")
            return replace_standards(standards[type][config], type)
        else:
            return config
    else:
        return config

def parse():
    initial_parse = config_file.initial_parse(path)
    return {key: replace_standards(value, key) for key, value in initial_parse.items()}
    return replace_standards(initial_parse)


    
