defaults = {
    'apt': {
        'packages': {
            'unattended-upgrades': {},
        },
        'sources': set(),
    },
    'monitoring': {
        'services': {
            'apt upgradable': {
                'vars.command': '/usr/lib/nagios/plugins/check_apt_upgradable',
                'vars.sudo': True,
                'check_interval': '1h',
            },
            'current kernel': {
                'vars.command': 'ls /boot/vmlinuz-* | sort -V | tail -n 1 | xargs -n1 basename | cut -d "-" -f 2- | grep -q "^$(uname -r)$"',
                'check_interval': '1h',
            },
            'apt reboot-required': {
                'vars.command': 'ls /var/run/reboot-required 2> /dev/null && exit 1 || exit 0',
                'check_interval': '1h',
            },
        },
    },
}
