defaults = {
    'apt': {
        'packages': {
            'dehydrated': {},
            'dnsutils': {},
        },
    },
    'letsencrypt': {
        'domains': {
            # 'example.com': {
            #     'aliases': {'www.example.com'},
            #     'reload': {'nginx'},
            #     'owner': 'www-data',
            #     'location': '/opt/app/certs',
            # },
        },
    },
    'systemd-timers': {
        'letsencrypt': {
            'command': '/usr/bin/dehydrated --cron --accept-terms --challenge dns-01',
            'when': 'daily',
        },
    },
}
