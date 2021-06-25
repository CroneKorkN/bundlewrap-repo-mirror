{
    'hostname': '162.55.188.157',
    'groups': [
        'archive',
        'hetzner-cloud',
        'debian-10',
        'mailserver',
        'webserver',
        'dnsserver',
    ],
    'bundles': [
        'wireguard',
        'nextcloud', #TEMP
        'influxdb2', #TEMP
        'zfs',
    ],
    'metadata': {
        'bind': {
            'domain': 'ns.sublimity.de',
            'zones': {
                'mail2.sublimity.de': [],
                'sublimity.de': [],
                'freibrief.net': [],
                'nadenau.net': [],
                'naeder.net': [],
                'rolfwerner.eu': [],
                'wettengl.net': [],
                'wingl.de': [],
                'woodpipe.de': [],
                'ckn.li': [],
            },
        },
        'id': 'ea29bdf0-0b47-4bf4-8346-67d60c9dc4ae',
        'network': {
            'interface': 'eth0',
            'ipv4': '162.55.188.157/32',
            'ipv6': '2a01:4f8:1c1c:4121::1/64',
        },
        'nginx': {
            'vhosts': {
                'nextcloud': {
                    'domain': 'test.ckn.li',
                    'ssl': 'letsencrypt',
                    'letsencrypt': {
                        'active': True,
                        'force_ssl': False,
                    },
                    'proxy': {
                        '/': {
                            'target':   'https://mail.sublimity.de:443',
                            'websocket': True,
                        },
                    },
                },
            },
        },
        'mailserver': {
            'hostname': 'mail2.sublimity.de',
            'admin_email': 'postmaster@sublimity.de',
            'domains': [
                'mail2.sublimity.de',
                # 'sublimity.de',
                # 'freibrief.net',
                # 'nadenau.net',
                # 'naeder.net',
                # 'rolfwerner.eu',
                # 'wettengl.net',
                # 'wingl.de',
                # 'woodpipe.de',
            ],
        },
        'nextcloud': {
            'version': '21.0.2',
            'sha256': '5e5b38109a3485db5fd2d248f24478eabe6c0790ec10b030acbbee207d5511fe',
        },
        'roundcube': {
            'product_name': 'Sublimity Mail',
            'version': '1.4.11',
            'installer': True,
        },
        'vm': {
            'cpu': 2,
        },
        'wireguard': {
            # ip r add 10.0.0.0/24 via 172.19.136.2 dev wg0
            'my_ip': '172.19.136.2/22',
            'peers': {
                'home.server': {
                    'route': [
                        '10.0.0.0/24',
                        '10.0.2.0/24',
                        '10.0.9.0/24',
                    ]
                },
            },
        },
        'zfs': {
            'pools': {
                'tank': {
                    'device': '/dev/disk/by-id/scsi-0HC_Volume_11764264',
                },
            },
        },
        'archive': {
            'paths': {
                '/var/test': {},
            },
        },
    },
}
