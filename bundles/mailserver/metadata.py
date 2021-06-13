database_password = repo.vault.password_for(f'{node.name} db mailserver')

defaults = {
    'mailserver': {
        'maildir': '/var/vmail',
        'database': {
            'host': '127.0.0.1',
            'name': 'mailserver',
            'user': 'mailserver',
            'password': database_password,
        },
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
    'zfs': {
        'datasets': {
            'tank/vmail': {
                'mountpoint': '/var/vmail',
                'compression': 'on',
            },
        },
    },
}
