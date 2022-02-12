defaults = {
    'systemd-timers': {
        'zfs-mirror': {
            'command': '/opt/zfs-mirror',
            'when': 'daily',
            'persistent': True,
        },
    },
}
