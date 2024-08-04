class ConfigCapellaProject:
    _conf: dict
    organization_id: str
    project_id: str

    def __init__(self, conf: dict):
        self._conf = conf
        self.organization_id = conf['organization_id']
        self.project_id = conf['project_id']

def generate_capella_projects(conf: dict) -> dict[str, ConfigCapellaProject]:
    return {cp_id: ConfigCapellaProject(cp) for cp_id, cp in conf['capella_projects'].items()}

