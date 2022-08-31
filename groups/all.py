{
    'bundles': [
        'system',
        'users',
    ],
    'metadata': {
        'dns': {},
        'nameservers': {
            '10.0.11.3',
        },
        'users': {
            'root': {
                'authorized_keys': {
                    'ssh-ed25519 AAAAC3NzaC1lZDI1NTE5AAAAIAi6tA8JaeovsxyvNNY0g5OEfErHThJHAOWVLguqvVve mwiegand@macbook',
                },
            },
        },
        'letsencrypt': {
            'acme_node': 'netcup.mails',
        },
    }
}
