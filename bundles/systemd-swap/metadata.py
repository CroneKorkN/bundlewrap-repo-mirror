defaults = {
    'systemd-swap': 2*10**9,
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
