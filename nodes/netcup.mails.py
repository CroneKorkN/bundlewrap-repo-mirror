{
    'hostname': '202.61.255.108',
    'groups': [
        'backup',
        'debian-11',
        'mailserver',
        'monitored',
        'webserver',
        'dnsserver',
    ],
    'bundles': [
        'bind-acme',
        'islamicstate.eu',
        'wireguard',
        'zfs',
    ],
    'metadata': {
        'id': 'ea29bdf0-0b47-4bf4-8346-67d60c9dc4ae',
        'network': {
            'internal': {
                'interface': 'eth1',
                'ipv4': '10.0.11.3/24',
            },
            'external': {
                'interface': 'eth0',
                'ipv4': '202.61.255.108/22',
                'gateway4': '202.61.252.1',
                'ipv6': '2a03:4000:55:a89::2/64',
                'gateway6': 'fe80::1',
            }
        },
        'bind': {
            'hostname': 'resolver.name',
            'acme_zone': 'acme.sublimity.de',
            'zones': {
                'sublimity.de',
                'freibrief.net',
                'nadenau.net',
                'naeder.net',
                'rolfwerner.eu',
                'wettengl.net',
                'wingl.de',
                'woodpipe.de',
                'ckn.li',
                'islamicstate.eu',
                'hausamsilberberg.de',
            },
        },
        'dns': {
            'ckn.li': {
                'A': ['202.61.255.108'],
                'AAAA': ['2a01:4f8:1c1c:4121::2'],
            },
            'sublimity.de': {
                'A': ['202.61.255.108'],
                'AAAA': ['2a01:4f8:1c1c:4121::2'],
            },
            'freibrief.net': {
                'A': ['202.61.255.108'],
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
            'domains': {
                'ckn.li',
                'sublimity.de',
                'freibrief.net',
                'nadenau.net',
                'naeder.net',
                'rolfwerner.eu',
                'wettengl.net',
                'wingl.de',
                'woodpipe.de',
            },
        },
        'rspamd': {
            'hostname': 'rspamd.sublimity.de',
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
            'version': '1.5.0',
            'installer': True,
        },
        'vm': {
            'cores': 4,
            'ram': 16384,
        },
        'wireguard': {
            'my_ip': '172.30.0.1/24',
            's2s': {
                'home.server': {
                    'allowed_ips': [
                        '10.0.0.0/24',
                        '10.0.2.0/24',
                        '10.0.9.0/24',
                    ],
                },
                'netcup.secondary': {
                    'allowed_ips': [
                        '10.0.11.0/24',
                    ],
                },
                'wb.offsite-backups': {
                    'allowed_ips': [
                        '192.168.178.0/24',
                    ],
                },
            },
            'clients': {
                'macbook': {
                    'peer_ip': '172.30.0.100/32',
                },
                'phone': {
                    'peer_ip': '172.30.0.101/32',
                },
                'ipad': {
                    'peer_ip': '172.30.0.102/32',
                },
            },
        },
        'zfs': {
            'pools': {
                'tank': {
                    'devices': [
                        '/dev/sda4',
                    ],
                },
            },
        },
    },
}
