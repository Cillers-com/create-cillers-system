from pathlib import Path
import importlib.util
from typing import Callable
from .. import filepaths

class ModelDirectoryChanges:
    path: Path
    data_structure_id: str

    def __init__(self, data_structure_id: str):
        self.data_structure_id = data_structure_id
        self.path = filepaths.COUCHBASE_CHANGES_ROOT / data_structure_id

    def all_ids(self) -> list[str]:
        return [f.stem for f in self.path.rglob('*.py')]

    def change_function(self, change_id: str) -> Callable:
        filename = f"{change_id}.py"
        filepath = self.path / filename
        assert filepath.exists()
        spec = importlib.util.spec_from_file_location(filename, filepath)
        module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)
        if not hasattr(module, 'change'):
            raise KeyError(f"change module 'couchbase.{self.data_structure_id}.{change_id}'"
                           " has no function 'change'")
        function = getattr(module, 'change')
        if not callable(function):
            raise KeyError(f"The change attribute in module 'couchbase.{self.data_structure_id}."
                           "{change_id}' is not callable")
        return function

    def ensure_exists(self):
        self.path.mkdir(parents=True, exist_ok=True)
