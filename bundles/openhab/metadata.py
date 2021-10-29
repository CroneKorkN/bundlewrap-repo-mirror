defaults = {
    'apt': {
        'packages': {
            'openhab': {
                'needs': [
                    'zfs_dataset:tank/openhab',
                ],
            },
        },
        'sources': {
            'deb https://openhab.jfrog.io/artifactory/openhab-linuxpkg stable main',
        },
    },
    'zfs': {
        'datasets': {
            'tank/openhab': {
                'mountpoint': '/var/lib/openhab',
            },
        },
    },
}
