{
    'hostname': '10.0.0.5',
    'groups': [
        'autologin',
        'backup-server',
        'debian-12',
        'home',
        'monitored',
    ],
    'bundles': [
        'grub',
        'smartctl',
        'wol-sleeper',
        'zfs',
        'zfs-mirror',
    ],
    'metadata': {
        'id': '9cf52515-63a1-4659-a8ec-6c3c881727e5',
        'network': {
            'internal': {
                'interface': 'enp0s31f6',
                'ipv4': '10.0.0.5/24',
                'gateway4': '10.0.0.1',
                'mac': '4c:cc:6a:d5:96:f8',
            },
        },
        'backup-server': {
            'hostname': 'backups.sublimity.de',
        },
        # 'smartctl': {
        #     '/dev/disk/by-id/ata-HGST_HDN726040ALE614_K3GV6TPL': {
        #         'apm': 1,
        #     },
        #     '/dev/disk/by-id/ata-HGST_HDN726040ALE614_K4KAJXEB': {
        #         'apm': 1,
        #     },
        #     '/dev/disk/by-id/ata-TOSHIBA_HDWQ140_19VZK0EMFAYG': {
        #         'apm': 1,
        #     },
        # },
        'ssh': {
            # multipling prevents server from sleeping
            'multiplex_incoming': False,
        },
        'wol-sleeper': {
            'network': 'internal',
            'waker': 'home.server',
        },
        'zfs-mirror': {
            'server': 'wb.offsite-backups',
        },
        'zfs': {
            'pools': {
                'tank': {
                    'type': 'raidz',
                    'devices': [
                        '/dev/disk/by-id/ata-HGST_HDN726040ALE614_K3GV6TPL',
                        '/dev/disk/by-id/ata-HGST_HDN726040ALE614_K4KAJXEB',
                        '/dev/disk/by-id/ata-TOSHIBA_HDWQ140_19VZK0EMFAYG',
                    ],
                },
            },
            'auto_snapshots': {
                'hourly': 1,
                'daily': 7,
                'weekly': 4,
                'monthly': 24,
            },
        },
    },
}
