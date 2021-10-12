{
    'hostname': '192.168.178.20',
    'groups': [
        'debian-11',
    ],
    'bundles': [
        'wireguard',
        'zfs',
    ],
    'metadata': {
        # TEMP
        'nameservers': {
            '8.8.8.8',
        },

        'id': '23b898bd-203b-42d5-8150-cdb459915d77',
        'network': {
            'internal': {
                'interface': 'eth0',
                'ipv4': '192.168.178.20/24',
                'gateway4': '192.168.178.1',
            },
        },
        'wireguard': {
            'my_ip': '172.30.0.4/32',
            's2s': {
                'htz.mails': {
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
                        '/dev/disk/by-id/ata-TOSHIBA_MG06ACA10TE_61C0A1B1FKQE',
                    ],
                },
            },
        },
    },
}
