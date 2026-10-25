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
        'systemd-mount',
        'systemd-timers',
        'users',
        'zsh',
    ],
    'metadata': {
        'dns': {},
        'hosts': {
            # the wireguard ips of the nameservers, reachable from every node
            '172.30.0.1': [
                'resolver.name',
            ],
            '172.30.0.3': [
                'secondary.resolver.name',
            ],
        },
        'letsencrypt': {
            'acme_node': 'ovh.mails',
        },
        'nameservers': {
            '172.30.0.1',
            '172.30.0.3',
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
            # agent sessions (ssh-grant): the key only works while a grant is active
            'mwiegand-agent': {
                'authorized_keys': {
                    'ssh-ed25519 AAAAC3NzaC1lZDI1NTE5AAAAIDeU8FKtjN1+VjhxKZTzyvJ51GzPevrScXgou08hFmjb mwiegand-agent',
                },
            },
        },
        'sudoers': {
            'ckn': {'ALL'},
            'mwiegand-agent': {'ALL'},
        },
    },
}
