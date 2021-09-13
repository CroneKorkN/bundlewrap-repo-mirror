defaults = {
    'apt': {
        'packages': {
            'jq': {},
            'rsync': {},
        },
    },
    'backup': {
        'server': None,
        'paths': set(),
    },
    'systemd-timers': {
        f'backup': {
            'command': '/opt/backup/backup_all',
            'when': 'daily',
        },
    },
}
