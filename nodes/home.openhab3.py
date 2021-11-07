{
    'hostname': '10.0.0.17',
    'groups': [
        'raspberry-pi',
        'debian-11',
        'monitored',
        'webserver',
    ],
    'bundles': [
        'zfs',
        'openhab',
        'java',
        'mirror',
    ],
    'metadata': {
        'FIXME_dont_touch_sshd': True,
        'telegraf': {
            'config': {
                'agent': {
                    'flush_interval': '30s',
                    'interval': '30s',
                },
            },
        },
        'id': '0afcde75-95c8-4fbd-b4c2-8a0fcc92884a',
        'network': {
            'internal': {
                'interface': 'eth0',
                'ipv4': '10.0.0.17/24',
                'gateway4': '10.0.0.1',
            },
        },
        'nginx': {
            'vhosts': {
                'openhab.ckn.li': {
                    'content': 'nginx/proxy_pass.conf',
                    'context': {
                        'target': 'http://localhost:8080',
                    },
                },
            },
        },
        'letsencrypt': {
            'domains': {
                'test11.ckn.li': {},
            }
        },
        'java': {
            'version': 11,
        },
        'zfs': {
            'pools': {
                'tank': {
                    'devices': [
                        '/dev/disk/by-id/mmc-SE32G_0x1766be0d-part3',
                    ],
                },
            },
        },
    },
}
