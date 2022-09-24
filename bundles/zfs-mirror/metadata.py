defaults = {
    'systemd-timers': {
        'zfs-mirror': {
            'command': '/opt/zfs-mirror',
            'when': '2:00',
            'persistent': True,
        },
    },
}
