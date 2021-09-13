{
    'hostname': '159.69.93.165',
    'groups': [
        'backup',
        'debian-11',
    ],
    'bundles': [
#        'steam',
#        'l4d2',
        'java',
        'minecraft',
    ],
    'metadata': {
        'id': '353bb086-f3ce-4f36-8533-e91786c91ed9',
        'network': {
            'internal': {
                'interface': 'ens10',
                'ipv4': '10.0.10.3/24',
            },
            'external': {
                'interface': 'eth0',
                'ipv4': '159.69.93.165/32',
                'ipv6': '2a01:4f8:c2c:867::2/64',
                'gateway4': '172.31.1.1',
                'gateway6': 'fe80::1',
            }
        },
        'minecraft': {
            'download': 'https://launcher.mojang.com/v1/objects/a16d67e5807f57fc4e550299cf20226194497dc2/server.jar',
            'sha256': 'e8c211b41317a9f5a780c98a89592ecb72eb39a6e475d4ac9657e5bc9ffaf55f',
        },
    },
}
