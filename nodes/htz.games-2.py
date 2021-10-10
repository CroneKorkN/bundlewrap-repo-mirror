{
    'hostname': '23.88.121.141',
    'groups': [
        'backup',
        'debian-11',
        'hetzner-cloud',
    ],
    'bundles': [
        'steam',
        'left4dead2',
#        'java',
#        'minecraft',
    ],
    'metadata': {
        'id': '3915f236-dd0a-4c6c-8fb3-1584c81038c6',
        'left4dead2': {
            'steamgroups': [38347879],
            'workshop': {
                '2524204971', # admin system inkl admin menu
            },
            'admins': {
                'STEAM_1:0:12376499', # CroneKorkN
            },
            'servers': {
                'realism-expert': {
                    'port': 27001,
                    'sv_steamgroup_exclusive': 1,
                    'map': 'c2m1_highway',
                },
            }
        },
        'network': {
            'internal': {
                'interface': 'ens10',
                'ipv4': '10.0.10.4/32',
            },
            'external': {
                'interface': 'eth0',
                'ipv4': '23.88.121.141/32',
                'ipv6': '2a01:4f8:c17:e0b4::2/64',
                'gateway4': '172.31.1.1',
                'gateway6': 'fe80::1',
            }
        },
    },
}
