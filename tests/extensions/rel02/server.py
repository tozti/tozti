foo_schema = {
        'attributes': {
            'foo': { 'type': 'string' },
            },
        'relationships': {
            "member": {
                "arity": "to-many",
                "type": "rel01/bar",
                }
            }
        }
bar_schema = {
        'attributes': {
            'bar': { 'type': 'string' },
            },
        'relationships': {
            }
        }
MANIFEST = {"types": {"foo": foo_schema, "bar": bar_schema}}
