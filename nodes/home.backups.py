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
                        # mdadm --create --metadata 1.0 --verbose /dev/md0 --level=stripe --raid-devices=2 /dev/disk/by-id/ata-WDC_WD30EZRX-00D8PB0_WD-WMC4N1776003 /dev/disk/by-id/ata-ST1750LM000_HN-M171RAD_S385J9EH700665
                        # ARRAY /dev/md/backups.home.ckn.li:0 metadata=1.0 name=backups.home.ckn.li:0 UUID=5209d078:d4d2db11:00ec4fcf:f4b71683
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
