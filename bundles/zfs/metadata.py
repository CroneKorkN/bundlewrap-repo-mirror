#import re

defaults = {
    'systemd-timers': {
        'zfs-trim': {
            'command': '/usr/lib/zfs-linux/trim',
            'when': 'Sat 00:00',
            'persistent': True,
        },
    },
}
