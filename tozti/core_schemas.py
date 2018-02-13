user_schema = {
    'attributes': {
        'name': { 'type': 'string' },
        'email': { 'type': 'string', 'format': 'email' },
        'login': { 'type': 'string' }
    },
    'relationships': {
        'groups': {
            'reverse-of': {
                'type': 'core/group',
                'path': 'members'
            }
        }
    }
}


group_schema = {
    'attributes': {
        'name': { 'type': 'string' }
    },
    'relationships': {
        'members': {
            'arity': 'to-many',
            'type': 'core/user'
        }
    }
}


SCHEMAS = {'user': user_schema,
           'group': group_schema,}
