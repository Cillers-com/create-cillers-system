import yaml
import os

def load_yaml(file_path):
    try:
        with open(file_path, 'r') as file:
            return yaml.safe_load(file) or {}
    except FileNotFoundError:
        return {}

def load_file(file, file_default):
    config = load_yaml(file)
    config.update(load_yaml(file_default))
    return config

def load():
    secrets = load_file(
        '../config/secrets_and_local_config/credentials.yml',
        '../config/credentials-public.yml')
    config = load_file(
        '../config/secrets_and_local_config/config-local.yml',
        '../config/config-shared.yml')

    os.environ['GOOGLE_API_KEY'] = secrets.get('google', {}).get('api_key', '')
    os.environ['GEMINI_API_KEY'] = secrets.get('google', {}).get('api_key', '')
    os.environ['COUCHBASE_USERNAME'] = secrets.get('couchbase', {}).get('username', '')
    os.environ['COUCHBASE_PASSWORD'] = secrets.get('couchbase', {}).get('password', '')
    os.environ['COUCHBASE_BUCKET_NAME'] = config.get('couchbase', {}).get('bucket_name', '')
    os.environ['COUCHBASE_URL'] = config.get('couchbase', {}).get('url', '')
    os.environ['REDPANDA_BOOTSTRAP_SERVERS'] = config.get('redpanda', {}).get('bootstrap_servers', '')
