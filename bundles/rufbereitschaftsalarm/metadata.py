defaults = {
    'apt': {
        'packages': {
            'gpiod': {},
        },
    },
    'flask': {

    },
    'systemd': {
        'units': {
            'rufbereitschaftsalarm-sound.service': {
                'Unit': {
                    'Description': 'rufbereitschaftsalarm sound effect',
                    'After': 'network.target',
                },
                'Service': {
                    'ExecStart': '/opt/rufbereitschaftsalarm-sound',
                },
                'Install': {
                    'WantedBy': {
                        'multi-user.target'
                    },
                },
            },
            'rufbereitschaftsalarm-stop.service': {
                'Unit': {
                    'Description': 'rufbereitschaftsalarm stop button',
                    'After': 'network.target',
                },
                'Service': {
                    'ExecStart': '/opt/rufbereitschaftsalarm-stop',
                },
                'Install': {
                    'WantedBy': {
                        'multi-user.target'
                    },
                },
            },
        },
    },
}
