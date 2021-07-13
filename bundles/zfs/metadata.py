#import re

defaults = {
    'systemd-timers': {
        'zfs-trim': {
            'command': '/usr/lib/zfs-linux/trim',
            'when': 'Sat 00:00',
            'persistent': True,
        },
        'zfs-scrub': {
            'command': '/usr/lib/zfs-linux/scrub',
            'when': 'Sun 00:00',
            'persistent': True,
        },
        'zfs-auto-snapshot-hourly': {
            'command': '/usr/sbin/zfs-auto-snapshot --quiet --syslog --label=hourly --keep=24 //',
            'when': 'hourly',
        },
        'zfs-auto-snapshot-daily': {
            'command': '/usr/sbin/zfs-auto-snapshot --quiet --syslog --label=daily --keep=7 //',
            'when': 'daily',
        },
        'zfs-auto-snapshot-weekly': {
            'command': '/usr/sbin/zfs-auto-snapshot --quiet --syslog --label=weekly --keep=4 //',
            'when': 'weekly',
            'persistent': True,
        },
        'zfs-auto-snapshot-monthly': {
            'command': '/usr/sbin/zfs-auto-snapshot --quiet --syslog --label=monthly --keep=24 //',
            'when': 'monthly',
            'persistent': True,
        },
    },
}
