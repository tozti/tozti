user_schema = {
    'attributes': {
        'name': { 'type': 'string' },
        'email': { 'type': 'string', 'format': 'email' },
        'handle': { 'type': 'string' },
    },
    'relationships': {
        'groups': {
            'arity': 'to-many',
            'type': 'core/group',
        },

        'pinned': {
            'arity': 'to-many',
            'type': 'core/folder'
        }
    }
}


group_schema = {
    'attributes': {
        'name': { 'type': 'string' },
        'handle': { 'type': 'string' },
    },

    'relationships': {
        'members': {
            'reverse-of': {
                'type': 'core/user',
                'path': 'groups'
            }
        },

        'groups': {
            'arity': 'to-many',
            'type': 'core/group',
        },

        'pinned': {
            'arity': 'to-many',
            'type': 'core/folder'
        }
    }
}

folder_schema = {
    'attributes': {
        'name': { 'type': 'string' }
    },

    'relationships': {
        'children': {
            'arity': 'to-many'
        },

        'parents': {
            'reverse-of': {
                'type': 'core/folder',
                'path': 'children'
            }
        }
    }
}


SCHEMAS = {
    'user': user_schema,
    'group': group_schema,
    'folder': folder_schema
}
