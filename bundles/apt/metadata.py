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
        },
    },
}
