{
    'dummy': True,
    'hostname': '159.69.93.165',
    'groups': [
        'backup',
        'debian-11',
        'hetzner-cloud',
    ],
    'bundles': [
       'steam',
#       'left4dead2',
        'java',
#        'minecraft',
    ],
    'metadata': {
        # TEMP
        'nameservers': {
            '8.8.8.8',
        },
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
        'id': '353bb086-f3ce-4f36-8533-e91786c91ed9',
        'network': {
            'interfaces': {
                'internal': {
                    'match': 'ens10',
                    'ipv4': '10.0.10.3/32',
                },
                'external': {
                    'match': 'eth0',
                    'ipv4': '159.69.93.165/32',
                    'ipv6': '2a01:4f8:c2c:867::2/64',
                    'gateway4': '172.31.1.1',
                    'gateway6': 'fe80::1',
                },
            },
        },
        'minecraft': {
            'download': 'https://launcher.mojang.com/v1/objects/a16d67e5807f57fc4e550299cf20226194497dc2/server.jar',
            'sha256': 'e8c211b41317a9f5a780c98a89592ecb72eb39a6e475d4ac9657e5bc9ffaf55f',
            'servers': {
                'test1': {
                    'rcon.password': '!decrypt:encrypt$gAAAAABhPyiZwNaanZ66yWGek-TXITmqQax1QU25hDgsRveJXe3AKKI6fP6f_XRvx1FZgixKMOaixgbgLcsJi_rY5IdZ5NZqIw==',
                },
            },
        },
    },
}
