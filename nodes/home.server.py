{
    'hostname': '10.0.0.2',
    'groups': [
#        'archive',
        'debian-10',
    ],
    'bundles': [
        'zfs',
    ],
    'metadata': {
        'id': 'af96709e-b13f-4965-a588-ef2cd476437a',
        'network': {
            'internal': {
                'interface': 'enp1s0f0',
                'ipv4': '10.0.0.2/24',
                'gateway4': '10.0.0.1',
            },
        },
        'users': {
            'root': {
                'shell': '/usr/bin/zsh',
            },
        },
        'vm': {
            'cores': 2,
            'ram':  16192,
        },
        'zfs': {
            'pools': {
                'tank': {
                    'mirrors': [
                        '/dev/disk/by-partlabel/zfs-data-1',
                        '/dev/disk/by-partlabel/zfs-data-2',
                    ],
                },
            },
        },
    },
}
