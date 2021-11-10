defaults = {
    'systemd-swap': {
        'size': 2*10**9,
    },
    'systemd': {
        'units': {
            'swapfile.swap': {
                'Swap': {
                    'What': '/swapfile',
                },
            },
        },
    },
}
