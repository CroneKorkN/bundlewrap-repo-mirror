{
    'hostname': '10.0.0.2',
    'groups': [
        'archive',
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
            },
        },
        'gitea': {
            'version': '1.14.2',
            'sha256': '0d11d87ce60d5d98e22fc52f2c8c6ba2b54b14f9c26c767a46bf102c381ad128',
            'domain': 'git.sublimity.de',
        },
        'wireguard': {
            # iptables -t nat -A POSTROUTING -o enp1s0f0 -j MASQUERADE
            'my_ip': '172.19.136.1/22',
            'peers': {
                'htz.mails': {},
            },
        },
    },
}
