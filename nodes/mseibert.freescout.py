{
    'dummy': True,
    'hostname': '159.69.117.89',
    'groups': [
        'backup',
        'debian-12',
        'monitored',
        'webserver',
        'freescout',
    ],
    'bundles': [
        'wireguard',
        'zfs',
    ],
    'metadata': {
        'id': '5333e3dd-0718-493a-a93c-529612a45079',
        'network': {
            'internal': {
                'interface': 'ens10',
                'ipv4': '10.0.227.2/24',
            },
            'external': {
                'interface': 'eth0',
                'ipv4': '159.69.117.89/32',
                'gateway4': '172.31.1.1',
                'ipv6': '2a01:4f8:c013:3d0b::1/64',
                'gateway6': 'fe80::1',
            },
        },
        'freescout': {
            'domain': 'foerderkreis.oranienschule-wiesbaden-wiki.de',
        },
        'vm': {
            'cores': 1,
            'ram': 2048,
        },
        'wireguard': {
            'my_ip': '172.30.0.238/32',
            's2s': {
                'netcup.mails': {
                    'allowed_ips': [
                        '10.0.0.0/24',
                        '10.0.2.0/24',
                        '10.0.9.0/24',
                        '10.0.10.0/24',
                        '10.0.11.0/24',
                    ],
                },
            },
        },
        'zfs': {
            'pools': {
                'tank': {
                    'devices': [
                        '/dev/disk/by-id/scsi-0HC_Volume_100662393',
                    ],
                },
            },
        },
    },
}
