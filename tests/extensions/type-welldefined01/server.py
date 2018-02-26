foo_schema = {
    'body': {
        'name': { 'type': 'string' },
        'email': { 'type': 'string', 'format': 'email' },
    }
}
MANIFEST = {"name": "type-welldefined01", "types": {"foo": foo_schema}}
