{
    'hostname': '10.0.99.126',
    'groups': [
        'autologin',
        'debian-12',
        'hardware',
        'home',
        'monitored',
    ],
    'bundles': [
        'kea-dhcpd',
        'wireguard',
    ],
    'metadata': {
        'id': '1d6a43e5-858c-42f9-9c40-ab63d61c787c',
        'network': {
            'internal': {
                'interface': 'eno1',
                'ipv4': '10.0.0.1/24',
                'vlans': {'iot', 'internet', 'guest'},
            },
            'temp': {
                'interface': 'enx00e04c220682',
                'ipv4': '10.0.99.126/24',
                'gateway4': '10.0.99.1',
            },
            'iot': {
                'type': 'vlan',
                'id': 2,
                'ipv4': '10.0.2.1/24',
            },
            'internet': {
                'type': 'vlan',
                'id': 3,
                'ipv4': '10.0.3.1/24',
            },
            'guest': {
                'type': 'vlan',
                'id': 9,
                'ipv4': '10.0.9.1/24',
            },
        },
        'kea': {
            'Dhcp4': {
                'interfaces-config': {
                    'interfaces': ['eno1', 'iot', 'guest'],
                },
                'subnet4': [
                    {
                        'subnet': '10.0.0.0/24',
                        'pools': [
                            { 'pool': '10.0.0.100 - 10.0.0.200' },
                        ],
                        'option-data': [
                            { 'name': 'routers', 'data': '10.0.0.1' },
                            { 'name': 'domain-name-servers', 'data': '10.0.10.2' },
                        ],
                    },
                    {
                        'subnet': '10.0.2.0/24',
                        'pools': [
                            { 'pool': '10.0.2.100 - 10.0.2.200' },
                        ],
                        'option-data': [
                            { 'name': 'routers', 'data': '10.0.2.1' },
                            { 'name': 'domain-name-servers', 'data': '10.0.10.2' },
                        ],
                    },
                    {
                        'subnet': '10.0.9.0/24',
                        'pools': [
                            { 'pool': '10.0.9.100 - 10.0.9.200' },
                        ],
                        'option-data': [
                            { 'name': 'routers', 'data': '10.0.9.1' },
                            { 'name': 'domain-name-servers', 'data': '10.0.10.2' },
                        ],
                    },
                ],
            },
        },
        'nftables': {
            'forward': {
                # Drop DHCP client requests (UDP port 68)
                'udp sport 68 drop',
                'udp dport 68 drop',

                # Drop DHCP server responses (UDP port 67)
                'udp sport 67 drop',
                'udp dport 67 drop',
            },
        },
        'sysctl': {
            'net': {
                'ipv4': {
                    'ip_forward': 1,
                },
            },
        },
        'wireguard': {
            'my_ip': '172.30.0.2/32',
            's2s': {
                'htz.mails': {
                    'allowed_ips': [
                        '10.0.10.0/24',
                        '10.0.10.0/24',
                        '192.168.179.0/24',
                        '10.0.227.0/24', # mseibert.freescout
                    ],
                },
            },
        },
    },
}
