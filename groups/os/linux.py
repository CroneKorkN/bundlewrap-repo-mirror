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
                'command': '/sbin/fstrim -v /',
                'when': 'daily',
            },
        },
        'hosts': {
            '10.0.11.3': [
                'resolver.name',
                'secondary.resolver.name',
            ],
        },
    },
}
