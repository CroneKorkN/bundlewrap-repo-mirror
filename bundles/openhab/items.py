directories = {
    '/var/lib/openhab': {
        'owner': 'openhab',
        'group': 'openhab',
        'needs': [
            'zfs_dataset:tank/openhab/data',
            'pkg_apt:openhab',
        ],
        'triggers': [
            'svc_systemd:openhab:restart',
        ],
    },
    '/etc/openhab': {
        'owner': 'openhab',
        'group': 'openhab',
        'needs': [
            'zfs_dataset:tank/openhab/config',
            'pkg_apt:openhab',
        ],
        'triggers': [
            'svc_systemd:openhab:restart',
        ],
    }
}


svc_systemd = {
    'openhab': {
        'needs': [
            'pkg_apt:openhab',
            'directory:/var/lib/openhab',
            'zfs_dataset:tank/openhab/config',
            'zfs_dataset:tank/openhab/data',
        ],
    }
}
