defaults = {
    'apt': {
        'packages': {},
        'sources': set(),
    },
    'monitoring': {
        'services': {
            'apt upgradable': {
                'vars.command': '/usr/lib/nagios/plugins/check_apt_upgradable',
                'vars.sudo': True,
                'check_interval': '1d',
            },
            'current kernel': {
                'vars.command': 'ls /boot/vmlinuz-* | sort -V | tail -n 1 | xargs -n1 basename | cut -d "-" -f 2- | grep -q "^$(uname -r)$"',
                'check_interval': '1h',
            },
        },
    },
}
