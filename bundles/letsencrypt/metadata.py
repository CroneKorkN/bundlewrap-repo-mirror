defaults = {
    'apt': {
        'packages': {
            'dehydrated': {},
        },
    },
    'cron': {
        'letsencrypt_renew': '{} 4 * * *    root    /usr/bin/dehydrated --cron --accept-terms --challenge http-01 > /dev/null'.format((node.magic_number % 60)),
        'letsencrypt_cleanup': '{} 4 * * 0    root    /usr/bin/dehydrated --cleanup > /dev/null'.format((node.magic_number % 60)),
    },
    'pacman': {
        'packages': {
            'dehydrated': {},
        },
    },
}
