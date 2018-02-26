foo_schema = {
        'body': {
            'foo': { 'type': 'string' },
            "members": {
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
MANIFEST = {"name": "rel02", "types": {"foo": foo_schema, "bar": bar_schema}}
