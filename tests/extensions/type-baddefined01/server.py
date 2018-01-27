foo_schema = {
    'attributes': {
        'name': { 'type': 'string' },
        'email': { 'type': 'string', 'format': 'email' },
    }
}
MANIFEST = {"types": {"foo": foo_schema}}
