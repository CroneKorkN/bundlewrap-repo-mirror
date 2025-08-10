{
    'hostname': '49.12.184.229',
    'groups': [
        'backup',
        'debian-13',
        'hetzner-cloud',
        'mailserver',
        'monitored',
        'webserver',
        'dnsserver',
        'wordpress',
    ],
    'bundles': [
        'bind-acme',
        'build-ci',
        'download-server',
        'islamicstate.eu',
        #'nginx-rtmps',
        'wireguard',
        'zfs',
    ],
    'metadata': {
        'id': 'ea29bdf0-0b47-4bf4-8346-67d60c9dc4ae',
        'network': {
            'internal': {
                'interface': 'enp7s0',
                'ipv4': '10.0.10.2/24',
            },
            'external': {
                'interface': 'eth0',
                'ipv4': '49.12.184.229/32',
                'gateway4': '172.31.1.1',
                'ipv6': '2a01:4f8:c013:51f2::1',
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
                'wettengl.net',
                'wingl.de',
                'woodpipe.de',
                'ckn.li',
                'islamicstate.eu',
                'hausamsilberberg.de',
                'wiegand.tel',
                'left4.me',
                'elimu-kwanza.de',
                'cronekorkn.de',
                'direkt.oranienschule.de',
                'foerderkreis.oranienschule-wiesbaden-wiki.de',
            },
        },
        'dns': {
            'ckn.li': {
                'A': ['49.12.184.229'],
                'AAAA': ['2a01:4f8:c013:51f2::1'],
            },
            'sublimity.de': {
                'A': ['49.12.184.229'],
                'AAAA': ['2a01:4f8:c013:51f2::1'],
            },
            'freibrief.net': {
                'A': ['49.12.184.229'],
                'AAAA': ['2a01:4f8:c013:51f2::1'],
            },
            'left4.me': {
                'A': ['49.12.184.229'],
                'AAAA': ['2a01:4f8:c013:51f2::1'],
            },
            'elimu-kwanza.de': {
                'TXT': ['google-site-verification=JwgcfXQ6nIXKxjMqUGHVBDISgMCQXgzMryPBsP2ZXnE'],
            },
        },
        'download-server': {
            'hostname': 'dl.sublimity.de',
        },
        'wordpress': {
            'elimukwanza': {
                'domain': 'elimu-kwanza.de',
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
            'dmarc_report_email': 'dmarc@sublimity.de',
            'domains': {
                'ckn.li',
                'sublimity.de',
                'freibrief.net',
                'nadenau.net',
                'naeder.net',
                'wettengl.net',
                'wiegand.tel',
                'left4.me',
                'elimu-kwanza.de',
            },
        },
        'dovecot': {
            'config_version': '2.4.1',
            'storage_version': '2.4.1',
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
                'cronekorkn.de': {
                    'content': 'nginx/redirect.conf',
                    'context': {
                        'target': 'https://www.twitch.tv/cronekorkn_',
                    },
                    'internal_dns': False,
                },
            },
        },
        'nginx-rtmps': {
            'hostname': 'rtmp.sublimity.de',
        },
        'roundcube': {
            'product_name': 'Sublimity Mail',
            'version': '1.6.11',
            'installer': False,
        },
        'vm': {
            'cores': 2,
            'ram': 4096,
        },
        'wireguard': {
            'my_ip': '172.30.0.1/24',
            's2s': {
                'home.router': {
                    'allowed_ips': [
                        '10.0.0.0/24',
                        '10.0.2.0/24',
                        '10.0.9.0/24',
                        '10.0.99.0/24',
                    ],
                },
                'ovh.secondary': {
                    'allowed_ips': [
                        '10.0.10.0/24',
                    ],
                },
                'wb.offsite-backups': {
                    'allowed_ips': [
                        '192.168.179.0/24',
                    ],
                },
                'mseibert.freescout': {
                    'allowed_ips': [
                        '10.0.227.0/24',
                    ],
                },
                'mseibert.yourls': {
                    'allowed_ips': [
                        '10.0.228.0/24',
                    ],
                },
                'mseibert.mailman': {
                    'allowed_ips': [
                        '10.0.229.0/24',
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
                        '/dev/disk/by-id/scsi-0HC_Volume_101332312',
                    ],
                },
            },
        },
    },
}
