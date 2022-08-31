{
    'hostname': '10.0.0.2',
    'groups': [
        'autologin',
        'backup',
        'debian-11',
        'home',
        'nextcloud',
        'monitored',
        'webserver',
        'hardware',
        'build-server',
    ],
    'bundles': [
        'apcupsd',
        'build-agent',
        'crystal',
        'gitea',
#        'gollum',
        'grafana',
        'icinga2',
        'icingaweb2',
        'influxdb2',
        'mirror',
        'postgresql',
        'redis',
        'smartctl',
        'steam-chat-logger',
        'steam-chat-viewer',
        'systemd-swap',
        'raspberrymatic-cert',
        'tasmota-charge',
        'wireguard',
        'wol-waker',
        'zfs',
    ],
    'metadata': {
        'id': 'af96709e-b13f-4965-a588-ef2cd476437a',
        'network': {
            'internal': {
                'interface': 'enp42s0',
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
            'version': '1.16.5',
            'sha256': 'c0fb4107dc4debf08e6e27fd3383e06dc232ccb410123179c7ae8d7cec60765f',
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
        'grub': {
            'kernel_params': {'nomodeset'}, # nvidia GT1030 freeze fix
        },
        'icinga2': {
            'hostname': 'icinga.sublimity.de',
        },
        'icingaweb2': {
            'hostname': 'icinga.sublimity.de',
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
            'version': '24.0.4',
        },
        'nextcloud-picsort': {
            'ckn': {
                'source': 'SofortUpload/AutoSort',
                'destination': 'Bilder/Chronologie',
                'unsortable': 'SofortUpload/Unsortable',
            },
        },
        'raspberrymatic-cert': {
            'domain': 'homematic.ckn.li',
            'node': 'home.homematic',
        },
        'steam_chat_logger': {
            'STEAM_USERNAME': 'snake_452',
            'STEAM_ID': 'STEAM_0:0:12376499',
            'STEAM_PASSWORD': '!decrypt:encrypt$gAAAAABiUzERrXVNxzDaDW_4MgEmPtXkMHlTiz5uqCbu-22-2yKHRHMKvuGqAygpGbnwZucZcmZMox9KM89a6qlVKlE1ZPizTA==',
            'IMAP_HOST': 'mail.sublimity.de',
            'IMAP_USER': 'i@ckn.li',
            'IMAP_PASSWORD': '!decrypt:encrypt$gAAAAABiUzcTVRL-Xb4RDjcwciZawYlmOa9Qy_hKz6sVWDlwZqUFLGRD8ERWoFCOWCM22Sq73Gc4nFuAblBB6wpbH5YEltLA6hmROGKpOFhI63ESLFwNgbY=',
        },
        'steam-chat-viewer': {
            'hostname': 'steam-chats.ckn.li',
        },
        'systemd-swap': 4_000_000_000,
        'tasmota-charge': {
            'phone': {
                'ip': '10.0.0.175',
                'user': 'u0_a233',
                'password': 'november',
            },
            'plug': {
                'ip': '10.0.2.115',
                'min': 45,
                'max': 70,
            },
        },
        'vm': {
            'cores': 16,
            'threads': 32,
            'ram':  49152,
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
            'zfs_arc_max_percent': 80,
            'storage_classes': {
                'ssd': 'ssd',
            },
            'pools': {
                'tank': {
                    'type': 'mirror',
                    'devices': [
                        '/dev/disk/by-partlabel/zfs-data-1',
                        '/dev/disk/by-partlabel/zfs-data-2',
                    ],
                },
                'ssd': {
                    'devices': [
                        '/dev/disk/by-id/nvme-SAMSUNG_MZVL22T0HBLB-00B00_S677NF0RA01551-part3',
                    ],
                },
                },
            'datasets': {
                'ssd/nextcloud-appdata': {
                    'mountpoint': '/var/lib/nextcloud/appdata_oci6dw1woodz',
                    'backup': False,
                }
            },
        },
    },
}
