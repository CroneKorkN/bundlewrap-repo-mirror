defaults = {
    'systemd-swap': 2*(2**30), # 2GiB
    'systemd': {
        'units': {
            'swapfile.swap': {
                'Swap': {
                    'What': '/swapfile',
                },
                'Install': {
                    'WantedBy': {
                        'swap.target',
                    },
                },
            },
        },
    },
}
