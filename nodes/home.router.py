{
    'hostname': '10.0.0.120',
    'groups': [
        # system
        'autologin',
        'debian-11',
        'hardware',
        'home',
        'monitored',
        # application
    ],
    'metadata': {
        'id': '1d6a43e5-858c-42f9-9c40-ab63d61c787c',
        'interfaces': {
            'internal': {
                'match': 'eno1',
                'ipv4': {
                    'addresses': {'10.0.0.120/24'},
                    'gateway4': '10.0.0.1',
                },
            },
            'wan': {
                'match': 'enx00e04c00135b',
                'dhcp': 'yes',
            },
        },
        'network': {
        },
    },
}
