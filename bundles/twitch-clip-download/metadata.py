defaults = {
    'backup': {
        'paths': {
            '/var/lib/twitch-clips',
        },
    },
    'systemd-timers': {
        f'twitch-clip-download': {
            'command': '/usr/local/bin/twitch-dl clips cronekorkn_ --download  --all',
            'when': 'daily',
            'persistent': True,
            'working_dir': '/var/lib/twitch-clips',
            'after': {
                'network-online.target',
            },
        },
    },
    'zfs': {
        'datasets': {
            'tank/twitch-clips': {
                'mountpoint': '/var/lib/twitch-clips',
                'needed_by': {
                    'svc_systemd:twitch-clip-download.timer',
                },
            },
        },
    },
}
