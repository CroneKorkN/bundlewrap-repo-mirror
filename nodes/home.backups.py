{
    'hostname': '10.0.0.5',
    'groups': [
        'debian-11',
        'backup-server',
        'monitored',
        'autologin',
    ],
    'bundles': [
        'smartctl',
        'wol-sleeper',
        'zfs',
        'zfs-mirror',
    ],
    'metadata': {
        'id': '9cf52515-63a1-4659-a8ec-6c3c881727e5',
        'network': {
            'internal': {
                'interface': 'enp1s0',
                'ipv4': '10.0.0.5/24',
                'gateway4': '10.0.0.1',
                'wol': True,
            },
        },
        'backup-server': {
            'hostname': 'backups.sublimity.de',
        },
        'smartctl': {
            '/dev/disk/by-id/ata-HGST_HDN726040ALE614_K3GV6TPL': {
                'apm': 1,
            },
            '/dev/disk/by-id/ata-HGST_HDN726040ALE614_K4KAJXEB': {
                'apm': 1,
            },
            '/dev/disk/by-id/ata-TOSHIBA_HDWQ140_19VZK0EMFAYG': {
                'apm': 1,
            },
        },
        'wol-sleeper': {
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
        },
    },
}
