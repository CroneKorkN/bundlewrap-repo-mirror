{
    'hostname': '51.68.189.180',
    'groups': [
        'debian-13',
        'dnsserver',
        'mailserver',
        'monitored',
        'webserver',
        'wordpress',
        # 'backup', # FIXME: from the switchover, until then htz.mails holds the data
    ],
    'bundles': [
        'download-server',
        'islamicstate.eu',
        'wireguard',
        'zfs',
        'systemd-swap',
        # 'bind-acme', # FIXME: from the switchover
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
            # FIXME: from the switchover, until then 10.0.10.2 is htz.mails, the resolver of all nodes
            # 'internal': {
            #     'interface': 'internal',
            #     'type': 'dummy',
            #     'ipv4': '10.0.10.2/24',
            # },
        },
        'systemd-swap': 2*2**30,
        'bind': {
            # FIXME: master from the switchover
            'master_node': 'htz.mails',
            'hostname': 'secondary.resolver.name',
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
        # FIXME: hub from the switchover, with the peers and clients of htz.mails
        'wireguard': {
            'my_ip': '172.30.0.3/32',
            's2s': {
                'htz.mails': {
                    'allowed_ips': [
                        '10.0.0.0/24',
                        '10.0.2.0/24',
                        '10.0.9.0/24',
                        '10.0.10.0/24',
                    ],
                },
            },
        },
        'zfs': {
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
