foo_schema = {
    'body': {
        'name': { 'type': 'string' },
        'email': { 'type': 'string', 'format': 'email' },
    },
}
MANIFEST = {"name": "type", "types": {"foo": foo_schema}}
