defaults = {
    'apt': {
        'packages': {
            'jq': {},
            'rsync': {},
        },
    },
    'backup': {
        'server': None,
        'paths': {},
    },
    'systemd-timers': {
        f'backup': {
            'command': '/opt/backup/backup_all',
            'when': 'daily',
        },
    },
}
