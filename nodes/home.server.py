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
        'grub',
        'grafana',
        'icinga2',
        'icingaweb2',
        'influxdb2',
        'mirror',
        'postgresql',
        'redis',
        'samba',
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
            'version': '1.17.1',
            'sha256': 'eafd476ee2a303d758448314272add00898d045439ab0d353ff4286c5e63496f',
            'domain': 'git.sublimity.de',
            'conf': {
                'mailer': {
                    'ENABLED': True,
                    'FROM': 'gitea@sublimity.de',
                    'MAILER_TYPE': 'smtp',
                    'HOST': 'mail.sublimity.de:587',
                    'USER': 'gitea@sublimity.de',
                    'PASSWD': '!decrypt:encrypt$gAAAAABjIlbZprmcIe_YktYgTU85VRSRz1MkyA7lNSDptWzGMrZ1N_YUXWoAIjWp4Lrmi8J0XYH9Pazhmz1vaIGUqUEsEnJXNh5n6-0Z0gcpePFC7x-Aj_M=',
                },
            },
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
            'version': '25.0.4',
            'config': {
                'instanceid': 'oci6dw1woodz',
                'secret': '!decrypt:encrypt$gAAAAABj96CFynVtEgsje7173zjQAcY7xQG3uyf5cxE-sJAvhyPh_KUykTKdwnExc8NTDJ8RIGUmVfgC6or5crnYaggARPIEg5-Cb0xVdEPPZ3oZ01ImLmynLu3qXT9O8kVM-H21--OKeztMRn7bySsbXdWEGtETFQ==',
                'passwordsalt': 'Zz/xed2SPxbkWh4/fajqYGhJ7Ps5R+',
            },
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
        'samba': {
            'shares': {
                'windows-backup': {},
            },
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
                'hdd': 'hdd',
            },
            'pools': {
                'tank': {
                    'type': 'mirror',
                    'devices': [
                        '/dev/disk/by-id/nvme-SAMSUNG_MZVL22T0HBLB-00B00_S677NF0RA01551-part1',
                        '/dev/disk/by-id/nvme-SAMSUNG_MZVL22T0HBLB-00B00_S677NF0RA01566-part1',
                    ],
                },
                'hdd': {
                    'type': 'mirror',
                    'devices': [
                        '/dev/disk/by-partlabel/zfs-data-1',
                        '/dev/disk/by-partlabel/zfs-data-2',
                    ],
                },
            },
            'datasets': {
                'tank/nextcloud-appdata': {
                    'mountpoint': '/var/lib/nextcloud/appdata_oci6dw1woodz',
                    'backup': False,
                },
                'hdd/nextcloud/ckn': {
                    'mountpoint': '/var/lib/nextcloud/ckn/files',
                },
                'hdd/nextcloud/ckn-privat': {
                    'mountpoint': '/var/lib/nextcloud/ckn-privat/files',
                },
            },
        },
    },
}
