files = {
    '/etc/apcupsd/apcupsd.conf': {
        'needs': [
            'pkg_apt:apcupsd',
        ],
    },
    '/usr/local/share/telegraf/apcupsd': {
        'source': 'telegraf_plugin',
        'mode': '755',
    },
}

svc_systemd = {
    'apcupsd': {
        'needs': [
            'pkg_apt:apcupsd',
            'file:/etc/apcupsd/apcupsd.conf',
        ],
    }
}
