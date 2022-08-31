{
    'supergroups': [
        'all',
    ],
    'bundles': [
        'hostname',
        'hosts',
        'htop',
        'locale',
        'network',
        'ssh',
        'sudo',
        'systemd',
        'systemd-journald',
        'systemd-networkd',
        'systemd-mount',
        'systemd-timers',
        'zsh',
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
        'users': {
            'ckn': {
                'shell': '/usr/bin/zsh',
                'authorized_keys': {
                    'ssh-ed25519 AAAAC3NzaC1lZDI1NTE5AAAAIAi6tA8JaeovsxyvNNY0g5OEfErHThJHAOWVLguqvVve mwiegand@macbook',
                },
            },
        },
        'sudoers': {
            'ckn': {'ALL'},
        },
    },
}
