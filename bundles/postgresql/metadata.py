defaults = {
    'postgresql': {
        'roles': {
            'root': {
                'password': repo.vault.password_for(f'{node.name} postgresql root'),
                'superuser': True,
                'needs': {
                    'svc_systemd:postgresql',
                },
            },
        },
        'databases': {},
    },
}

if node.has_bundle('zfs'):
    defaults['zfs'] = {
        'datasets': {
            'tank/postgresql': {
                'mountpoint': '/var/lib/postgresql',
            },
        },
    }
