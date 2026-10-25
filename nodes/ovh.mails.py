{
    'hostname': '51.68.189.180',
    'groups': [
        'backup',
        'debian-13',
        'dnsserver',
        'mailserver',
        'monitored',
        'webserver',
        'wordpress',
    ],
    'bundles': [
        'bind-acme',
        'download-server',
        'islamicstate.eu',
        'wireguard',
        'zfs',
        'systemd-swap',
    ],
    'metadata': {
        'id': 'd5080b1a-b310-48be-bd5a-02cfcecf0c90',
        'network': {
            'external': {
                'interface': 'ens3',
                'ipv4': '51.68.189.180/32',
                'gateway4': '51.68.188.1',
                'ipv6': '2001:41d0:701:1100::751a/128',
                'gateway6': '2001:41d0:701:1100::1',
                'cake': {
                    'Bandwidth': '350M',
                    'FlowIsolationMode': 'triple',
                    'PriorityQueueingPreset': 'besteffort',
                    'RTTSec': '100ms',
                },
            },
        },
        'systemd-swap': 2*2**30,
        'bind': {
            'hostname': 'resolver.name',
            'acme_zone': 'acme.sublimity.de',
            # spamhaus answers queries from ovh networks with 127.255.255.254, so ask through htz.secondary
            'forward_zones': {
                'spamhaus.org': {
                    '172.30.0.3',
                },
            },
            'zones': {
                'sublimity.de',
                'freibrief.net',
                'nadenau.net',
                'naeder.net',
                'wettengl.net',
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
                'A': ['51.68.189.180'],
                'AAAA': ['2001:41d0:701:1100::751a'],
            },
            'sublimity.de': {
                'A': ['51.68.189.180'],
                'AAAA': ['2001:41d0:701:1100::751a'],
            },
            'freibrief.net': {
                'A': ['51.68.189.180'],
                'AAAA': ['2001:41d0:701:1100::751a'],
            },
            'left4.me': {
                'A': ['141.95.32.8'],
                'AAAA': ['2001:41d0:700:5508::1'],
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
                'hcf.ckn.li': { # hochzeit carina fabi
                    'content': 'nginx/redirect.conf',
                    'context': {
                        'target': 'https://cloud.sublimity.de/s/4xjDLnoH3tmCm3T',
                    },
                    'internal_dns': False,
                },
            },
        },
        'roundcube': {
            'product_name': 'Sublimity Mail',
            'version': '1.7.5',
            'installer': False,
        },
        'sysctl': {
            'net': {
                'ipv4': {
                    'ip_forward': 1,
                    'conf': {
                        'default': {
                            'forwarding': 1,
                        },
                    },
                },
                'ipv6': {
                    'conf': {
                        'all': {
                            'forwarding': 1,
                        },
                        'default': {
                            'forwarding': 1,
                        },
                    },
                },
            },
        },
        'vm': {
            'cores': 4,
            'ram': 8192,
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
                'htz.secondary': {},
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
                'ovh.left4me': {},
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
            # php, postgres and rspamd need the rest; the old server starved its arc below 1G
            'zfs_arc_max_percent': 40,
            'kernel_params': {
                'zfs_arc_min': str(2**30),
            },
            'pools': {
                'tank': {
                    'devices': [
                        '/dev/disk/by-partlabel/tank',
                    ],
                },
            },
        },
    },
}
