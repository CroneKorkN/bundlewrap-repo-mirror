{
    'hostname': '10.0.0.2',
    'groups': [
        'backup',
        'debian-11',
        'nextcloud',
        'monitored',
        'webserver',
    ],
    'bundles': [
        'gitea',
        'grafana',
        'influxdb2',
        'mirror',
        'postgresql',
        'redis',
        'wireguard',
        'zfs',
        'gollum',
    ],
    'metadata': {
        'id': 'af96709e-b13f-4965-a588-ef2cd476437a',
        'network': {
            'internal': {
                'interface': 'enp1s0f0',
                'ipv4': '10.0.0.2/24',
                'gateway4': '10.0.0.1',
            },
        },
        'gitea': {
            'version': '1.15.5',
            'sha256': '0d11d87ce60d5d98e22fc52f2c8c6ba2b54b14f9c26c767a46bf102c381ad128',
            'domain': 'git.sublimity.de',
        },
        'gollum': {
            'domain': 'wiki.sublimity.de',
            'wiki': 'https://git.sublimity.de/cronekorkn/wiki.git',
            'version': '5.2.3',
        },
        'grafana': {
            'hostname': 'grafana.sublimity.de',
            'influxdb_node': 'home.server',
        },
        'influxdb': {
            'hostname': 'influxdb.sublimity.de',
            'admin_token': '!decrypt:encrypt$gAAAAABg3z5PcaLYmUpcElJ07s_G-iYwnS8d532TcR8xUYbZfttT-B736zgR6J726mzKAFNYlIfJ7amNLIzi2ETDH5TAXWsOiAKpX8WC_dPBAvG3uXGtcPYENjdeuvllSagZzPt0hCIZQZXg--Z_YvzaX9VzNrVAgGD-sXQnghN5_Vhf9gVxxwP---VB_6iNlsf61Nc4axoS',
            'readonly_token': '!decrypt:encrypt$gAAAAABg3z1-0hnUdzsfivocxhJm58YnPLn96OUvnHiPaehdRhKd6TZBgEPc5YyR07t2-GEUfOvEwoie-O6QsVhWYxrwxNTBXux_iUSx7W6e-fLQA_3MgWf5G97q_3kx_wCgQ6V0iKRyxH988TpNSMACfS4WhCXdSes1CaMpic4VV3S3ox_gCrSHxO7yVXQkJDnOW0MixY5T',
            'writeonly_token': '!decrypt:encrypt$gAAAAABg3z6fGrOy2tNdo03RoYAXmpJoJYkfhBfpblPh_wxYfqmdjtABaD7XyV9mSh9xl8oWQlTAtCk9KndVCDQy7BJ-ju7S3HCKJ0k244Y5YKxUnQtqt9fc9nnm8XD-NOJqLKyfy0QhL_I8dFT02pygoJeCUR5NkZcTKf6julb-iGXI6vWcQgolJTYrW643pHObd-Z-vIEl',
        },
        'letsencrypt': {
            'delegate_to_node': 'htz.mails',
        },
        'nextcloud': {
            'hostname': 'cloud.sublimity.de',
            'version': '21.0.5',
        },
        'nextcloud-picsort': {
            'ckn': {
                'source': 'SofortUpload/AutoSort',
                'destination': 'Bilder/Chronologie',
            },
        },
        'users': {
            'root': {
                'shell': '/usr/bin/zsh',
            },
        },
        'vm': {
            'cores': 2,
            'ram':  16192,
        },
        'wireguard': {
            'my_ip': '172.30.0.2/32',
            's2s': {
                'htz.mails': {
                    'allowed_ips': [
                        '10.0.10.0/24',
                        '10.0.11.0/24',
                        '10.0.20.0/24',
                        '192.168.178.0/24',
                    ],
                },
            },
        },
        'zfs': {
            'pools': {
                'tank': {
                    'type': 'mirror',
                    'devices': [
                        '/dev/disk/by-partlabel/zfs-data-1',
                        '/dev/disk/by-partlabel/zfs-data-2',
                    ],
                },
            },
        },
    },
}
