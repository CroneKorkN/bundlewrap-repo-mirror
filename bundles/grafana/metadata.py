postgres_password = repo.vault.password_for(f'{node.name} postgres role grafana')

defaults = {
    'apt': {
        'packages': {
            'grafana': {},
        },
        'sources': [
            'deb https://packages.grafana.com/oss/deb stable main',
        ],
    },
    'grafana': {
        'config': {
            'server': {
                'http_port': 3370,
            },
            'database': {
                'url': f'postgres://grafana:{postgres_password}@localhost:5432/grafana',
            },
            'remote_cache': {
                'type': 'redis',
                'connstr': 'addr=127.0.0.1:6379',
            },
            'security': {
                'admin_user': 'admin',
                'admin_password': str(repo.vault.password_for(f'{node.name} grafana admin')),
            },
            'users': {
                'allow_signup': False,
            },
        },
    },
    'postgresql': {
        'databases': {
            'grafana': {
                'owner': 'grafana',
            },
        },
        'roles': {
            'grafana': {
                'password': postgres_password,
            },
        },
    },
    'zfs': {
        'datasets': {
            'tank/grafana': {
                'mountpoint': '/var/lib/grafana'
            },
        },
    },
}
