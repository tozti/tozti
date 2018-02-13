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


"""
Hash of the user's password (SHA256)
The hash is represented by a utf-8 encoded bytestring
"""

#TODO : add salt to the hash
user_password_schema = {
    'attributes': {
        'hash': {'type': 'string'},
        'login': {'type': 'string'} 
    },
    'relationships': {
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
           'group': group_schema,
           'user_password':user_password_schema}
