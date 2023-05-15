files = {
    '/opt/rufbereitschaftsalarm': {
        'mode': '550',
    },
}

svc_systemd = {
    'rufbereitschaftsalarm.service': {
        'enabled': False,
        'running': False,
        'needs': [
            'pkg_apt:gpiod',
            'file:/opt/rufbereitschaftsalarm',
        ],
    }
}
