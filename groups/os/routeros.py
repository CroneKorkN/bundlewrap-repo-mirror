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
        'grafana_rows': {
            'routeros_discards',
            'routeros_errors',
            'routeros_throughput',
            'routeros_poe',
            'routeros_packets',
            'routeros_health',
        },
        'routeros': {
            'gateway': '10.0.0.1',
            'bridge_priority': '0x8000',
            'ports': {},
            'vlans': {
                'home': '1',
                'iot': '2',
                'internet': '3',
                'proxmox': '4',
                'wokeonlan': '5',
                'gast': '9',
                'rolf': '51',
            },
            'vlan_groups': {
                'home': {
                    'untagged': 'home',
                    'tagged': set(),
                },
                'infra': {
                    'untagged': 'home',
                    'tagged': {
                        'iot',
                        'internet',
                        'proxmox',
                        'gast',
                        'rolf',
                        'wokeonlan',
                    },
                },
                'internet': {
                    'untagged': 'internet',
                    'tagged': set(),
                },
                'wokeonlan': {
                    'untagged': 'wokeonlan',
                    'tagged': set(),
                },
            },
            'vlan_ports': {},
        },
        'telegraf': {
            'influxdb_node': 'home.server',
        },
    },
    'os': 'routeros',
}
