{
    'hostname': '10.0.0.2',
    'groups': [
        'debian-10',
    ],
    'bundles': [
        'gitea',
        'postgresql',
        'wireguard',
        'gcloud',
    ],
    'metadata': {
        'network': {
            'interface': 'enp1s0f0',
            'ipv4': '10.0.0.2/24',
        },
        'gitea': {
            'version': '1.14.2',
            'sha256': '0d11d87ce60d5d98e22fc52f2c8c6ba2b54b14f9c26c767a46bf102c381ad128',
            'domain': 'git.sublimity.de',
        },
        'wireguard': {
            'my_ip': '172.19.136.1/22',
            'peers': {
                'htz.mails': {},
            },
        }, 
    },
}
