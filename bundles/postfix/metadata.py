database_password = repo.vault.password_for(f'{node.name} db mailserver')

defaults = {
    'apt': {
        'packages': {
            'postfix': {},
        }
    },
    'postfix': {
        'database': {
            'host': '127.0.0.1',
            'name': 'mailserver',
            'user': 'mailserver',
            'password': database_password,
        }
    },
    'postgresql': {
        'roles': {
            'mailserver': {
                'password': database_password,
            },
        },
        'databases': {
            'mailserver': {
                'owner': 'mailserver',
            },
        },
    },
}
