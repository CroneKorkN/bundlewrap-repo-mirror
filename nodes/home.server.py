{
    'hostname': '10.0.0.2',
    'groups': [
        'backup',
        'debian-11',
        'nextcloud',
        'monitored',
        'webserver',
        'hardware',
        'build-server',
    ],
    'bundles': [
        'build-agent',
        'gitea',
        'gollum',
        'grafana',
        'influxdb2',
        'mirror',
        'mosquitto',
        'postgresql',
        'redis',
        'smartctl',
        'wireguard',
        'zfs',
        'crystal',
        'tasmota-charge',
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
        'build-server': {
            'hostname': 'build.sublimity.de',
            'architectures': {
                'amd64': {
                    'node': 'home.server',
                    'target': 'x86_64-unknown-linux-gnu',
                },
                'arm64': {
                    'node': 'home.openhab',
                    'target': 'aarch64-unknown-linux-gnu',
                },
            },
            'download_server': 'netcup.mails',
        },
        'gitea': {
            'version': '1.15.5',
            'sha256': 'c3f190848c271bf250d385b80c1a98a7e2c9b23d092891cf1f7e4ce18c736484',
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
        'mosquitto': {
            'hostname': 'mqtt.sublimity.de',
            'users': {
                'openhab': {},
            },
        },
        'nextcloud': {
            'hostname': 'cloud.sublimity.de',
            'version': '21.0.5',
        },
        'nextcloud-picsort': {
            'ckn': {
                'source': 'SofortUpload/AutoSort',
                'destination': 'Bilder/Chronologie',
                'unsortable': 'SofortUpload/Unsortable',
            },
        },
        'tasmota-charge': {
            'phone': {
                'ip': '10.0.0.166',
                'user': 'u0_q194',
                'password': 'november',
            },
            'plug': {
                'ip': '10.0.2.115',
                'min': 45,
                'max': 70,
            },
        },
        'vm': {
            'cores': 2,
            'ram':  16192,
        },
        'wireguard': {
            'my_ip': '172.30.0.2/32',
            's2s': {
                'netcup.mails': {
                    'allowed_ips': [
                        '10.0.10.0/24',
                        '10.0.11.0/24',
                        '192.168.179.0/24',
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
