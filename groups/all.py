{
    'bundles': [
        'sudo',
        'system',
        'users',
        'zsh',
    ],
    'metadata': {
        'dns': {},
        'nameservers': {
            '10.0.11.3',
        },
        'users': {
            'root': {
                'shell': '/usr/bin/zsh',
                'authorized_keys': {
                    'ssh-ed25519 AAAAC3NzaC1lZDI1NTE5AAAAIEU1l2ijW3ZqzFGZcdWg2ESgTGehdNfBTfafxsjWvWdS mwiegand@macbook',
                },
            },
        },
        'letsencrypt': {
            'acme_node': 'netcup.mails',
        },
    }
}
