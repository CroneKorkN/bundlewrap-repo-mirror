defaults = {
    'apt': {
        'packages': {
            'gpiod': {},
        },
    },
    'systemd': {
        'units': {
            'stromzaehler.service': {
                'Unit': {
                    'Description': 'stromzaehler',
                    'After': 'network.target',
                },
                'Service': {
                    'ExecStart': '/opt/stromzaehler',
                },
                'Install': {
                    'WantedBy': {'multi-user.target'},
                },
            },
        },
    },
}
