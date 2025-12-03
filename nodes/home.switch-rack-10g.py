{
    'hostname': '10.0.0.63',
    'username': 'admin',
    'password': '!decrypt:encrypt$gAAAAABoYFUx2faf18aV3rzNNuBA-4xZ22LQJ2HinpgsjkoTQS_l2TbmDtiAZI1jt-kWfTZ48d5_UPX-VDmY9qb4Sgn2Iz7Yee3CrB4hl85TyutilukTIP8=',
    'groups': [
        'routeros',
    ],
    'metadata': {
        'id': '26eca3f1-975e-426f-bd7d-e2a1ef36519e',
        'routeros': {
            'ips': {
                '10.0.0.63/24': {
                    'interface': 'home',
                },
            },
            'ports': {
                'sfp-sfpplus1': {
                    'vlan_group': 'infra',
                    'comment': 'home.router',
                },
                'sfp-sfpplus2': {
                    'vlan_group': 'infra',
                    'comment': 'home.server',
                },
                'sfp-sfpplus3': {
                    'vlan_group': 'home',
                    'comment': 'home.backups',
                },
                'sfp-sfpplus4': {
                    'vlan_group': 'home',
                },
                'sfp-sfpplus5': {
                    'vlan_group': 'home',
                },
                'sfp-sfpplus6': {
                    'vlan_group': 'home',
                },
                'sfp-sfpplus7': {
                    'vlan_group': 'home',
                },
                'sfp-sfpplus8': {
                    'vlan_group': 'infra',
                    'comment': 'home.switch-vorratsraum-poe',
                },
                'ether1': {
                    'vlan_group': 'infra',
                    'comment': 'home.switch-rack-poe',
                },
            },
        },
    },
}
