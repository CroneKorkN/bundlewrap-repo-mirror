{
    'hostname': '10.0.0.17',
    'groups': [
        'backup',
        'debian-11',
        'monitored',
        'raspberry-pi',
        'webserver',
        'autologin',
    ],
    'bundles': [
        'build-agent',
        'java',
        'openhab',
        'systemd-swap',
        'zfs',
    ],
    'metadata': {
        'FIXME_dont_touch_sshd': True,
        'id': '34199b24-4621-42f4-85ae-ec354f9c43e6',
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
        'java': {
            'version': 11,
        },
        'zfs': {
            'pools': {
                'tank': {
                    'devices': [
                        '/dev/mmcblk1p3',
                    ],
                },
            },
        },
    },
}
