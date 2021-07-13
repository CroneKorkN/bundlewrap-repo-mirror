defaults = {
    'apt': {
        'packages': {
            'postfix': {},
            'postfix-pgsql': {},
        }
    },
    'backup': {
        'paths': {
            '/var/vmail',
        },
    },
    'letsencrypt': {
        'reload_after': {
            'postfix',
        }, 
    },
    'telegraf': {
        'config': {
            'inputs': {
                'postfix': [{}],
            },
        },
    },
}
