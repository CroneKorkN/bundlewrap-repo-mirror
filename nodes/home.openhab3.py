{
    'hostname': '10.0.0.17',
    'groups': [
        'raspberry-pi',
        'debian-11',
        'monitored',
    ],
    'bundles': [
        'zfs',
        'openhab',
        'java',
    ],
    'metadata': {
        'id': '0afcde75-95c8-4fbd-b4c2-8a0fcc92884a',
        'network': {
            'internal': {
                'interface': 'eth0',
                'ipv4': '10.0.0.17/24',
                'gateway4': '10.0.0.1',
            },
        },
        'zfs': {
            'pools': {
                'tank': {
                    'devices': [
                        '/dev/disk/by-id/mmc-SE32G_0x1766be0d-part3',
                    ],
                },
            },
        },
    },
}
