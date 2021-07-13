{
    'hostname': '10.0.0.2',
    'bundles': [
        'systemd',
        'systemd-timers',
        'zfs',
    ],
    'metadata': {
        'os_release': 'buster',
        'id': 'af96709e-b13f-4965-a588-ef2cd476437a',
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
    'os_version': (10,),
    'os': 'debian',
    'pip_command': 'pip3',
}
