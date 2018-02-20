user_schema = {
    'body': {
        'name': {
            'type': 'string'
        },
        'email': {
            'type': 'string',
            'format': 'email'
        },
        'login': {
            'type': 'string'
        },
        'groups': {
            'type': 'relationship',
            'arity': 'auto',
            'pred-type': 'core/group',
            'pred-relationship': 'members',
        }
    }
}


group_schema = {
    'body': {
        'name': {
            'type': 'string'
        },
        'members': {
            'type': 'relationship',
            'arity': 'to-many',
            'targets': 'core/user'
        }
    }
}


SCHEMAS = {'user': user_schema,
           'group': group_schema,}
