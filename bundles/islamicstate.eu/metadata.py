defaults = {
    'nginx': {
        'vhosts': {
            'islamicstate.eu': {
                'content': 'nginx/html.conf',
                'context': {
                    'root': '/var/www/islamicstate.eu',
                },
            }
        },
    },
}
