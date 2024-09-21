{
    'supergroups': [
        'all',
    ],
    'bundles': [
        'hostname',
        'hosts',
        'htop',
        'linux',
        'locale',
        'network',
        'ssh',
        'sudo',
        'system',
        'systemd',
        'systemd-journald',
        'systemd-networkd',
        'systemd-mount',
        'systemd-timers',
        'users',
        'zsh',
    ],
    'metadata': {
        'dns': {},
        'hosts': {
            '10.0.10.2': [
                'resolver.name',
                'secondary.resolver.name',
            ],
        },
        'letsencrypt': {
            'acme_node': 'htz.mails',
        },
        'nameservers': {
            '10.0.10.2',
        },
        'systemd-timers': {
            'trim': {
                'command': '/sbin/fstrim -v /',
                'when': 'daily',
            },
        },
        'users': {
            'root': {
                'authorized_keys': {
                    'ssh-ed25519 AAAAC3NzaC1lZDI1NTE5AAAAILMVroYmswD4tLk6iH+2tvQiyaMe42yfONDsPDIdFv6I ckn',
                },
            },
            'ckn': {
                'shell': '/usr/bin/zsh',
                'authorized_keys': {
                    'ssh-ed25519 AAAAC3NzaC1lZDI1NTE5AAAAILMVroYmswD4tLk6iH+2tvQiyaMe42yfONDsPDIdFv6I ckn',
                },
            },
        },
        'sudoers': {
            'ckn': {'ALL'},
        },
    },
}
