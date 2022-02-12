{
    'metadata': {
        'systemd': {
            'units': {
                'getty@tty1.service.d/override.conf': {
                    'Service': {
                        'ExecStart': [
                            '',
                            '-/usr/sbin/agetty --autologin root --noclear %I $TERM',
                        ],
                    },
                },
            },
            'services': {
                'getty@tty1.service': {},
            },
            'logind': {
                'NAutoVTs': 1,
            },
        },
    },
}
