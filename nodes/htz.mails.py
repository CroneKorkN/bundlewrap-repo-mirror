{
    'hostname': '162.55.188.157',
    'groups': [
        'backup',
        'hetzner-cloud',
        'debian-11',
        'mailserver',
        'monitored',
        'webserver',
        'dnsserver',
    ],
    'bundles': [
        'islamicstate.eu',
        'wireguard',
        'zfs',
    ],
    'metadata': {
        'id': 'ea29bdf0-0b47-4bf4-8346-67d60c9dc4ae',
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
        'bind': {
            'hostname': 'resolver.name',
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
                'hausamsilberberg.de': [],
            },
        },
        'dns': {
            'ckn.li': {
                'A': ['162.55.188.157'],
                'AAAA': ['2a01:4f8:1c1c:4121::2'],
            },
            'freibrief.net': {
                'A': ['162.55.188.157'],
                'AAAA': ['2a01:4f8:1c1c:4121::2'],
            },
        },
        'letsencrypt': {
            'domains': {
                'ckn.li': {},
                'sublimity.de': {},
                'freibrief.net': {},
            },
        },
        'mailserver': {
            'hostname': 'mail.sublimity.de',
            'admin_email': 'postmaster@sublimity.de',
            'domains': [
                'ckn.li',
                'sublimity.de',
                'freibrief.net',
                'nadenau.net',
                'naeder.net',
                'rolfwerner.eu',
                'wettengl.net',
                'wingl.de',
                'woodpipe.de',
            ],
        },
        'nginx': {
            'vhosts': {
                'cloud.sublimity.de': {
                    'content': 'nginx/proxy_pass.conf',
                    'context': {
                        'target': 'https://cloud.sublimity.de:443',
                    },
                    'internal_dns': False,
                },
                'git.sublimity.de': {
                    'content': 'nginx/proxy_pass.conf',
                    'context': {
                        'target': 'https://git.sublimity.de:443',
                    },
                    'internal_dns': False,
                },
                'grafana.sublimity.de': {
                    'content': 'nginx/proxy_pass.conf',
                    'context': {
                        'target': 'https://grafana.sublimity.de:443',
                    },
                    'internal_dns': False,
                },
                'influxdb.sublimity.de': {
                    'content': 'nginx/proxy_pass.conf',
                    'context': {
                        'target': 'https://influxdb.sublimity.de:443',
                    },
                    'internal_dns': False,
                },
                'hausamsilberberg.de': {
                    'content': 'nginx/redirect.conf',
                    'context': {
                        'target': 'https://www.internationaler-bund.de/standort/204516',
                    },
                    'internal_dns': False,
                },
            },
        },
        'roundcube': {
            'product_name': 'Sublimity Mail',
            'version': '1.5-rc',
            'installer': True,
        },
        'users': {
            'root': {
                'authorized_users': [
                    'root@home.server',
                ],
                'authorized_keys': {
                    'ecdsa-sha2-nistp256 AAAAE2VjZHNhLXNoYTItbmlzdHAyNTYAAAAIbmlzdHAyNTYAAABBBHMKTJLw6Cb+MLt+9JFOkuo2QBpuA8EoTKOFpb3IFQHEq19YLMzOhcErWmzaRfiCnILhnwTQz0njS+n9Qu4aghk= root@mail.sublimity.de'
                },
            },
        },
        'vm': {
            'cores': 2,
            'ram': 8096,
        },
        'wireguard': {
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
                'wb.offsite-backups': {
                    'route': [
                        '10.0.20.0/24',
                    ],
                },
            },
        },
        'zfs': {
            'pools': {
                'tank': {
                    'device': '/dev/disk/by-id/scsi-0QEMU_QEMU_HARDDISK_drive-scsi0-0-0-0-part2',
                },
            },
        },
    },
}
