{
    'hostname': '49.12.184.229',
    'groups': [
        'backup',
        'debian-13',
        'dnsserver',
        'monitored',
    ],
    'bundles': [
        'wireguard',
        'systemd-swap',
    ],
    'metadata': {
        'id': 'ea29bdf0-0b47-4bf4-8346-67d60c9dc4ae',
        'network': {
            'external': {
                'interface': 'eth0',
                'ipv4': '49.12.184.229/32',
                'gateway4': '172.31.1.1',
                'ipv6': '2a01:4f8:c013:51f2::1',
                'gateway6': 'fe80::1',
            }
        },
        'systemd-swap': 4*2**30,
        'bind': {
            'master_node': 'ovh.mails',
            'hostname': 'secondary.resolver.name',
        },
        'vm': {
            'cores': 2,
            'ram': 4096,
        },
        'wireguard': {
            'my_ip': '172.30.0.3/32',
            's2s': {
                'ovh.mails': {
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
