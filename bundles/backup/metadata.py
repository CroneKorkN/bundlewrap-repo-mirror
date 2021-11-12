defaults = {
    'apt': {
        'packages': {
            'jq': {
                'needed_by': {
                    'svc_systemd:backup.timer',
                },
            },
            'rsync': {
                'needed_by': {
                    'svc_systemd:backup.timer',
                },
            },
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
