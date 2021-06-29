{
    'hostname': '10.0.0.2',
    'groups': [
        'archive',
        'backup',
        'debian-10',
#        'nextcloud',
    ],
    'bundles': [
        'gitea',
        'postgresql',
        'wireguard',
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
        'gitea': {
            'version': '1.14.2',
            'sha256': '0d11d87ce60d5d98e22fc52f2c8c6ba2b54b14f9c26c767a46bf102c381ad128',
            'domain': 'git.sublimity.de',
        },
        'users': {
            'root': {
                'shell': '/usr/bin/zsh',
            },
        },
        'wireguard': {
            'my_ip': '172.30.0.2/24',
            'peers': {
                'htz.mails': {
                    'route': [
                        '10.0.10.0/24',
                        '10.0.11.0/24',
                    ],
                },
            },
        },
    },
}
