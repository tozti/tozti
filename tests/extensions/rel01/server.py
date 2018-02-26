foo_schema = {
        'body': {
            'foo': { 'type': 'string' },
            "member": {
                "type": "relationship",
                "arity": "to-one",
                "targets": "rel01/bar",
                }
            }
        }
bar_schema = {
        'body': {
            'bar': { 'type': 'string' },
            }
        }
MANIFEST = {"name": "rel01", "types": {"foo": foo_schema, "bar": bar_schema}}
