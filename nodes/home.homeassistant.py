{
    'hostname': '10.0.0.16',
    'groups': [
        'autologin',
        'backup',
        'debian-12',
        'hardware',
        'home',
        'monitored',
        'raspberry-pi',
        'webserver',
    ],
    'bundles': [
        'homeassistant',
        'zfs',
    ],
    'metadata': {
        'id': '3d67964d-1270-4d3c-b93f-9c44219b3d59',
        'network': {
            'internal': {
                'interface': 'eth0',
                'ipv4': '10.0.0.16/24',
                'gateway4': '10.0.0.1',
            },
        },
        'homeassistant': {
            'domain': 'homeassistant.ckn.li',
        },
        'zfs': {
            'pools': {
                'tank': {
                    'devices': [
                        '/var/lib/zfs/tank.img',
                    ],
                },
            },
        },
    },
}
