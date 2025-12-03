{
    'hostname': '10.0.0.62',
    'username': 'admin',
    'password': '!decrypt:encrypt$gAAAAABoYFSyt2JAsdePXiHim1RdQwbarJedhAOE3XpS2rGMBx-F5eCWRCIyLU2g2ocUDUIDfgH3nBipUCkdcd0Bv4vbK-yqKmGSeSH7YXLYwq3ZWuCDsLM=',
    'groups': [
        'routeros',
    ],
    'metadata': {
        'id': '6d4b95dd-5d8a-4481-8c5f-8ee714d9f0cc',
        'routeros': {
            'ips': {
                '10.0.0.62/24': {
                    'interface': 'home',
                },
            },
            'ports': {
                'ether1': {
                    'vlan_group': 'infra',
                    'comment': 'home.switch-vorratsraum-poe',
                },
                'ether2': {
                    'vlan_group': 'infra',
                    'comment': 'wohnzimmer-ap',
                },
                'ether3': {
                    'vlan_group': 'home',
                    'comment': 'gaming-pc',
                },
                'ether4': {
                    'vlan_group': 'infra',
                    'comment': 'schreibtisch-dock',
                },
                'ether5': {
                    'vlan_group': 'infra',
                    'comment': 'switch-wohnzimmer-unifi',
                },
            },
        },
    },
}
