defaults = {
    'apt': {
        'packages': {
            'redis-server': {},
        },
    },
    'backup': {
        'paths': {
            '/var/lib/redis',
        },
    }
}

if node.has_bundle('zfs'):
    defaults['zfs'] = {
        'datasets': {
            'tank/redis': {
                'mountpoint': '/var/lib/redis',
                'needed_by': [
                    'pkg_apt:redis-server',
                    'directory:/var/lib/redis',
                ],
            },
        },
    }
