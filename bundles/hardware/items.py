files = {
    '/usr/local/share/icinga/plugins/cpu_frequency': {
        'mode': '0755',
        'triggers': {
            'svc_systemd:telegraf:restart',
        },
    },
}
