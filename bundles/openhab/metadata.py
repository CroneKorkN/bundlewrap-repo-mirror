defaults = {
    'apt': {
        'packages': {
            'openhab': {
                'needs': [
                    'zfs_dataset:tank/openhab/config',
                    'zfs_dataset:tank/openhab/data',
                ],
            },
        },
        'sources': {
            'jfrog': {
                'urls': {
                    'https://openhab.jfrog.io/artifactory/openhab-linuxpkg',
                },
                'suites': {
                    'stable',
                },
                'components': {
                    'main',
                },
            },
        },
    },
    'zfs': {
        'datasets': {
            'tank/openhab': {
                'mountpoint': 'none',
            },
            'tank/openhab/config': {
                'mountpoint': '/etc/openhab',
            },
            'tank/openhab/data': {
                'mountpoint': '/var/lib/openhab',
            },
        },
    },
}
