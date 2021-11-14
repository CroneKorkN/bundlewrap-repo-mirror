{
    'supergroups': [
        'all',
    ],
    'bundles': [
        'hostname',
        'hosts',
        'locale',
        'network',
        'ssh',
        'systemd',
        'systemd-journald',
        'systemd-networkd',
        'systemd-mount',
        'systemd-timers',
    ],
    'metadata': {
        'systemd-timers': {
            'trim': {
                'command': '/usr/sbin/fstrim -v /',
                'when': 'daily',
            },
        },
        'hosts': {
            '10.0.11.3': [
                'resolver.name',
                'first.resolver.name',
                'second.resolver.name',
            ],
        },
    },
}
