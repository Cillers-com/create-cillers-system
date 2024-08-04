import urllib
import time
from couchbase.cluster import Cluster
from couchbase.diagnostics import ServiceType
from ..base import connection
from ..config.config_cluster import ConfigCluster
from ...shared.config.config_credentials import ConfigCredentialsUnion, ConfigCredentialsBasic
from .model_data_structure import ModelDataStructure
from .model_metadata import ModelMetadata

class ModelCluster:
    cluster: Cluster
    conf: ConfigCluster
    metadata = ModelMetadata
    data_structures: dict[str, ModelDataStructure]

    def __init__(self, conf: ConfigCluster):
        self.conf = conf
        self.ensure_cluster_initialized()
        self.cluster = connection.get_cluster(self.params_client_change())
        service_types = [
            ServiceType.Management,
            ServiceType.KeyValue,
            ServiceType.Query]
        connection.wait_until_ready(self.cluster, service_types, 5*60)
        self.metadata = ModelMetadata(
            self.cluster,
            conf.shared.metadata,
            conf.bucket_settings_metadata)
        self.metadata.ensure_initialized()
        self.data_structures = {}
        for ds_id, conf_ds in self.conf.shared.data_structures.items():
            self.data_structures[ds_id] = ModelDataStructure(
                self.cluster,
                ds_id,
                conf_ds,
                self.metadata)

    def change(self):
        for _, model_ds in self.data_structures.items():
            model_ds.change()

    def ensure_cluster_initialized(self):
        encoded_data = urllib.parse.urlencode(self.params_cluster_init()['data']).encode()
        request = urllib.request.Request(
            self.conf.params_cluster_init['url'],
            data=encoded_data,
            method='POST')
        max_retries = 30
        for attempt in range(max_retries):
            try:
                with urllib.request.urlopen(request, timeout=5*60) as response:
                    response_body = response.read().decode()
                    print(f"cluster initialization successful: {response_body}")
                return
            except Exception as e:
                if attempt == max_retries - 1:
                    print('Max retries exceeded')
                    raise e
                error_message = str(e)
                if 'already initialized' in error_message or 'Unauthorized' in error_message:
                    print("Cluster was already initialized.")
                    return
                print(f"The cluster is not responding. Retrying SHOULDN'T HAVE TO ... {e}")
                time.sleep(1)
        assert False

    def connection_string(self) -> str:
        return f"{self.conf.connection.protocol}://{self.conf.connection.host}"

    def credentials_change(self) -> ConfigCredentialsUnion:
        return self.conf.credentials.get(self.conf.credentials_id_change)

    def params_credentials_change(self) -> dict:
        c = self.credentials_change()
        assert isinstance(c, ConfigCredentialsBasic)
        return {
            'username': c.username,
            'password': c.password}

    def params_client_change(self) -> dict:
        return {
            'connection_string': self.connection_string(),
            'credentials': self.params_credentials_change()}

    def params_cluster_init(self) -> dict:
        return {
            'url': f"http://{self.conf.connection.host}:8091/clusterInit",
            'data': {
                'username': self.conf.credentials_change.username,
                'password': self.conf.credentials_change.password,
                'services': ','.join(self.conf.shared.services),
                'hostname': '127.0.0.1',
                'memoryQuota': '256',
                'sendStats': 'false',
                'clusterName': 'cillers',
                'setDefaultMemQuotas': 'true',
                'indexerStorageMode': 'plasma',
                'port': 'SAME'}}

