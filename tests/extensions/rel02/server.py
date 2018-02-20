foo_schema = {
        'body': {
            'foo': { 'type': 'string' },
            "member": {
                "type": "relationship",
                "arity": "to-many",
                "targets": "rel02/bar",
                }
            }
        }
bar_schema = {
        'body': {
            'bar': { 'type': 'string' },
            }
        }
MANIFEST = {"types": {"foo": foo_schema, "bar": bar_schema}}
