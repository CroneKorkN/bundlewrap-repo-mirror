{
    'hostname': '162.55.188.157',
    'groups': [
        'debian-10',
        'mailserver',
        'webserver',
    ],
    'bundles': [
        'zfs',
    ],
    'metadata': {
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
            'admin_email': 'postmaster@sublimity.de',
            'hostname': 'mail.sublimity.de',
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
