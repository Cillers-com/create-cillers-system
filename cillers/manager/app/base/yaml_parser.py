import os
from pathlib import Path
from typing import Union
import yaml
from .. import filepaths

def yaml_env_constructor(loader, node) -> str:
    value = loader.construct_scalar(node)
    return os.getenv(value)

def yaml_ref_constructor(loader, node) -> str:
    value = loader.construct_scalar(node)
    if not isinstance(value, str):
        raise ValueError(f"Illegal ref: '{value}' is not a string")
    return f"__cillers_reference__{value}"
    
yaml.SafeLoader.add_constructor('!env', yaml_env_constructor)
yaml.SafeLoader.add_constructor('!ref', yaml_ref_constructor)

def lookup(keypath: list, references: dict) -> any:
    key = keypath[0]
    if key not in references:
        raise KeyError(f"'{key}' is not a valid reference.")
    value = references[key]
    if len(keypath) == 1:
        return value
    return lookup(keypath[1:], value)

def _resolve_references(data: Union[dict, list], key: Union[str, int], references: dict):
    value = data[key]
    if isinstance(value, str) and value.startswith('__cillers_reference__'):
        v = lookup(value[21:].split('.'), references)
        data[key] = v 
    if isinstance(data[key], dict) or isinstance(data[key], list):
        resolve_references(data[key], references)

def resolve_references(data: any, references: dict) -> None: 
    if isinstance(data, dict):
        for k in data:
            _resolve_references(data, k, references)
    elif isinstance(data, list):
        for i in range(len(data)):
            _resolve_references(data, i, references)

def merge_unpacking_keys(data: any) -> None:
    if isinstance(data, dict) and '__**' in data:
        v = data.pop('__**')
        if not isinstance(v, dict):
            raise ValueError(f"Illegal unpacking value: '{v}' is not a dict.")
        data.update(v)
        merge_unpacking_keys(data)
    elif isinstance(data, dict):
        for v in data.values():
            merge_unpacking_keys(v)
    elif isinstance(data, list):
        for i in data:
            merge_unpacking_keys(i)

def process_filepaths(paths: dict[str, str], source_filepath: Path) -> None:
    for k, v in paths.items():
        if v.startswith('/'):
            paths[k] = filepaths.CONF_ROOT / v[1:]
        else:
            paths[k] = source_filepath.parent / v
        if not os.path.isfile(paths[k]):
            raise ValueError(f"The file '{paths[k]}' does not exist. Specified for import '{k}'")

def load_imports(paths: dict[str, Path]) -> None:
    for k, v in paths.items():
        paths[k] = load(v)

def pop_specs(data: any) -> dict:
    if isinstance(data, dict):
        v = data.pop('__specs', {})
        if not isinstance(v, dict):
            raise ValueError("'__specs' must be a key-value dictionary")
        if '__specs' in v:
            raise KeyError("'__specs' keyword is not allowed in __specs section.")
        return v
    return {}

def pop_and_load_imports(data: any, source_filepath: Path) -> dict:
    if isinstance(data, dict):
        v = data.pop('__imports', {})
        if '__specs' in v:
            raise KeyError("'__specs' keyword is not allowed as an import.")
        if not isinstance(v, dict):
            raise ValueError("'__imports' must be a key-value dictionary")
        for _v in v.values():
            if not isinstance(_v, str):
                raise ValueError("Values in the __imports section must be filepaths.")
        process_filepaths(v, source_filepath)
        load_imports(v)
        return v
    return {}

def load(filepath: Path) -> any:
    with open(filepath, 'r', encoding='utf-8') as file:
        data = yaml.safe_load(file)
    imports = pop_and_load_imports(data, filepath)
    specs = pop_specs(data)
    references = {'specs': specs, **imports}
    resolve_references(data, references)
    merge_unpacking_keys(data)
    return data

