{
    'hostname': '162.55.188.157',
    'groups': [
        'debian-10',
        'mailserver',
        'webserver',
    ],
    'bundles': [
        'wireguard',
        'zfs',
    ],
    'metadata': {
         'interfaces': {
            'eth0': {
                'ips': {
                    '162.55.188.157',
                    '2a01:4f8:1c1c:4121::/64',
                },
                'gateway4': '172.31.1.1',
                'gateway6': 'fe80::1',
            },
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
            'my_ip': '172.19.136.2/22',
            'peers': {
                'home.server': {},
            },
        },
        'zfs': {
            'pools': {
                'tank': {
                    'device': '/dev/disk/by-id/scsi-0HC_Volume_11764264',
                },
            },
        },
    },
}
