defaults = {
    'apt': {
        'packages': {
            'grafana': {},
        },
        'sources': [
            'deb https://packages.grafana.com/oss/deb stable main',
        ],
    },
    'postgresql': {
        'databases': {
            'grafana': {
                'owner': 'grafana',
            },
        },
        'roles': {
            'grafana': {
                'password': repo.vault.password_for(f'{node.name} postgres role grafana'),
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
