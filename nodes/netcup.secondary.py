{
    'hostname': '46.38.240.85',
    'groups': [
        'debian-10',
        'dnsserver',
        'monitored',
    ],
    'bundles': [
        'wireguard',
    ],
    'metadata': {
        'id': '890848b2-a900-4f74-ad5b-b811fbb4f0bc',
        'network': {
            'external': {
                'interface': 'eth0',
                'ipv4': '46.38.240.85/22',
                'gateway4': '46.38.240.1',
                'ipv6': '2a03:4000:7:534::2/64',
                'gateway6': 'fe80::1',
            },
            'internal': {
                'interface': 'eth1',
                'ipv4': '10.0.11.2/24',
            },
        },
        'bind': {
            'master_node': 'htz.mails',
            'hostname': 'second.resolver.name',
        },
        # 'postfix': {
        #     'master_node': 'htz.mails',
        #     'hostname': 'mail2.sublimity.de',
        # },
        'wireguard': {
            'my_ip': '172.30.0.3/32',
            's2s': {
                'htz.mails': {
                    'allowed_ips': [
                        '10.0.0.0/24',
                        '10.0.2.0/24',
                        '10.0.9.0/24',
                        '10.0.10.0/24',
                        '10.0.20.0/24',
                    ],
                },
            },
        },
    },
}
