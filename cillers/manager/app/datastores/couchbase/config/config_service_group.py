class ConfigServiceGroup:
    _conf: dict

    def __init__(self, conf: dict):
        self._conf = conf

def generate_service_groups(conf: dict):
    return {sg_id: ConfigServiceGroup(sg_conf) for sg_id, sg_conf in conf.items()}

