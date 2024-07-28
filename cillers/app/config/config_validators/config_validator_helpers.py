def get_subdict_reference_keys(conf):
    assert isinstance(conf, dict)
    return set(conf[next(iter(conf))].keys())

def assert_subdicts_have_same_keys(conf):
    assert isinstance(conf, dict)
    reference_keys = get_subdict_reference_keys(conf)
    for _, value in conf.items():
        assert set(value.keys()) == reference_keys

def assert_list_of_strings(conf):
    assert isinstance(conf, list)
    for item in conf:
        assert isinstance(item, str)

def assert_valid_dict(conf, schema):
    assert isinstance(conf, dict)
    assert isinstance(schema, dict)
    for key, spec in schema.items():
        optional = key.endswith('?')
        clean_key = key[:-1] if optional else key
        value = conf.get(clean_key, None)
        if value is None:
            if optional:
                continue
            assert False
        if callable(spec):
            spec(value)
        elif isinstance(spec, type):
            assert isinstance(value, spec)
        else:
            assert value == spec
    schema_keys = {k[:-1] if k.endswith('?') else k for k in schema.keys()}
    assert not set(conf.keys()) - set(schema_keys)

def assert_valid_typed_dict(conf, type_schemas, shared_schema = None):
    if shared_schema is None:
        shared_schema = {}
    assert 'type' in conf
    t = conf['type']
    assert t in type_schemas
    schema = {**shared_schema, **type_schemas[t]}
    conf_without_type = {key: value for key, value in conf.items() if key != 'type'}
    assert_valid_dict(conf_without_type, schema)
