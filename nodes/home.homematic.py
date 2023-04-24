{
    'dummy': True,
    'hostname': '10.0.2.8',
    'groups': [
        'autologin',
        'home',
        'raspberrymatic',
    ],
    'bundles': [
        'hostname',
    ],
    'metadata': {
        'id': 'cc1c08ba-8a2e-4cda-9b82-1b88a940e8e8',
        'network': {
            'interfaces': {
                'internal': {
                    'ipv4': '10.0.2.8/24',
                },
            },
        },
        'dns': {
            'homematic.ckn.li': {
                'A': {'10.0.2.8'},
            },
        },
        'users': {
            'root': {
                'authorized_users': {
                    'root@home.server',
                },
            },
        },
    },
}
