files = {
    '/usr/local/share/telegraf/cpu_frequency': {
        'mode': '0755',
        'triggers': {
            'svc_systemd:telegraf.service:restart',
        },
    },
}
