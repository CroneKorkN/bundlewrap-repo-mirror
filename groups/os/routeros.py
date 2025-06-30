# https://ftp-master.debian.org/keys.html

{
    'username': 'admin',
    'supergroups': [
        'all',
    ],
    'bundles': [
        'routeros',
    ],
    'metadata': {
        'routeros': {
            'gateway': '10.0.0.1',
            'bridge_priority': '0x8000',
            'ports': {},
            'vlans': {
                'home': '1',
                'iot': '2',
                'internet': '3',
                'proxmox': '4',
                'gast': '9',
                'rolf': '51',
            },
            'vlan_groups': {
                'infra': {
                    'untagged': 'home',
                    'tagged': {
                        'iot',
                        'internet',
                        'proxmox',
                        'gast',
                        'rolf',
                    },
                },
            },
            'vlan_ports': {},
            'ips': {
                '10.0.0.62/24': {
                    'interface': 'home',
                },
            },
        },
    },
    'os': 'routeros',
}
