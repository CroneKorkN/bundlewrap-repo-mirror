{
    'hostname': '162.55.188.157',
    'groups': [
        'archive',
        'backup',
        'hetzner-cloud',
        'debian-10',
        'mailserver',
        'monitored',
        'webserver',
        'dnsserver',
    ],
    'bundles': [
        'nextcloud',
        'wireguard',
        'zfs',
    ],
    'metadata': {
        'systemd-timers': {
            'test1': {
                'when': 'weekly',
                'command': '/bin/ls',
            },
        },
        'nextcloud': {
            'hostname': 'cloud.sublimity.de',
            'version': '21.0.0',
        },
        'id': 'ea29bdf0-0b47-4bf4-8346-67d60c9dc4ae',
        'bind': {
            'hostname': 'ns.sublimity.de',
            'zones': {
                'sublimity.de': [],
                'freibrief.net': [],
                'nadenau.net': [],
                'naeder.net': [],
                'rolfwerner.eu': [],
                'wettengl.net': [],
                'wingl.de': [],
                'woodpipe.de': [],
                'ckn.li': [],
                'islamicstate.eu': [],
            },
        },
        'dns': {
            'islamicstate.eu': {
                'A': ['1.2.3.4'],
            },
            'test.islamicstate.eu': {
                'AAAA': ['::1337'],
            },
        },
        'network': {
            'internal': {
                'interface': 'ens10',
                'ipv4': '10.0.10.2/24',
            },
            'external': {
                'interface': 'eth0',
                'ipv4': '162.55.188.157/32',
                'ipv6': '2a01:4f8:1c1c:4121::2/64',
                'gateway4': '172.31.1.1',
                'gateway6': 'fe80::1',
            }
        },
        # 'nginx': {
        #     'vhosts': {
        #         'nextcloud': {
        #             'domain': 'test.ckn.li',
        #             'ssl': 'letsencrypt',
        #             'letsencrypt': {
        #                 'active': True,
        #                 'force_ssl': False,
        #             },
        #             'proxy': {
        #                 '/': {
        #                     'target':   'https://mail.sublimity.de:443',
        #                     'websocket': True,
        #                 },
        #             },
        #         },
        #     },
        # },
        'mailserver': {
            'hostname': 'mail.sublimity.de',
            'admin_email': 'postmaster@sublimity.de',
            'domains': [
                'mail3.sublimity.de',
                'islamicstate.eu',
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
        'roundcube': {
            'product_name': 'Sublimity Mail',
            'version': '1.4.11',
            'installer': True,
        },
        'users': {
            'root': {
                'authorized_users': [
                    'root@home.server',
                ],
            },
        },
        'vm': {
            'cores': 2,
            'ram': 8096,
        },
        'wireguard': {
            # ip r add 10.0.0.0/24 via 172.19.136.2 dev wg0
            'my_ip': '172.30.0.1/24',
            'peers': {
                'home.server': {
                    'route': [
                        '10.0.0.0/24',
                        '10.0.2.0/24',
                        '10.0.9.0/24',
                    ],
                },
                'netcup.secondary': {
                    'route': [
                        '10.0.11.0/24',
                    ],
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
