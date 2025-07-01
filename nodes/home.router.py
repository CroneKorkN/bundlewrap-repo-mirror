{
    'hostname': '10.0.0.1',
    'groups': [
        'autologin',
        'debian-12',
        'hardware',
        'home',
        'monitored',
        #'dnsserver',
    ],
    'bundles': [
        'kea-dhcpd',
        'wireguard',
    ],
    'metadata': {
        'id': '1d6a43e5-858c-42f9-9c40-ab63d61c787c',
        'network': {
            'internal': {
                'interface': 'enp1s0f0',
                'ipv4': '10.0.0.1/24',
                'vlans': {'iot', 'internet', 'guest', 'rolf', 'proxmox'},
                'dhcp_server': True,
            },
            'iot': {
                'type': 'vlan',
                'id': 2,
                'ipv4': '10.0.2.1/24',
                'dhcp_server': True,
            },
            'external': {
                'type': 'vlan',
                'id': 3,
                'ipv4': '10.0.99.126/24',
                'gateway4': '10.0.99.1',
            },
            'proxmox': {
                'type': 'vlan',
                'id': 4,
                'ipv4': '10.0.4.1/24',
                'dhcp_server': True,
            },
            'guest': {
                'type': 'vlan',
                'id': 9,
                'ipv4': '10.0.9.1/24',
                'dhcp_server': True,
            },
            'rolf': { # rolf local test
                'type': 'vlan',
                'id': 51,
                'ipv4': '192.168.179.1/24',
                'dhcp_server': True,
            },
        },
        # 'bind': {
        #     'master_node': 'htz.mails',
        #     'hostname': 'home.resolver.name',
        # },
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
                        #'192.168.179.0/24', # while raspi at home
                        '10.0.227.0/24', # mseibert.freescout
                        '10.0.228.0/24', # mseibert.yourls
                        '10.0.229.0/24', # mseibert.mailsman
                    ],
                },
            },
        },
    },
}
