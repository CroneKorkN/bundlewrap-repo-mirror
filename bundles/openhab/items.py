directories = {
    '/var/lib/openhab': {
        'owner': 'openhab',
        'group': 'openhab',
        'needs': [
            'zfs_dataset:tank/openhab',
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
        ],
    }
}
