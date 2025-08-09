{
    'hostname': '135.125.239.125',
    'groups': [
        'debian-12',
        'dnsserver',
        'monitored',
    ],
    'bundles': [
        'wireguard',
    ],
    'metadata': {
        'id': 'd5080b1a-b310-48be-bd5a-02cfcecf0c90',
        'network': {
            'external': {
                'interface': 'ens3',
                'ipv4': '135.125.239.125/32',
                'gateway4': '135.125.238.1',
                'ipv6': '2001:41d0:701:1100::3dea/56',
                'gateway6': '2001:41d0:701:1100::1',
            },
        },
        'bind': {
            'master_node': 'htz.mails',
            'hostname': 'secondary.resolver.name',
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
                    ],
                },
            },
        },
    },
}
