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
                    'ssh-ed25519 AAAAC3NzaC1lZDI1NTE5AAAAILMVroYmswD4tLk6iH+2tvQiyaMe42yfONDsPDIdFv6I ckn',
                },
            },
        },
        'letsencrypt': {
            'acme_node': 'netcup.mails',
        },
    }
}
