defaults = {
    'apt': {
        'packages': {
            'postfix': {},
            'postfix-pgsql': {},
        }
    },
    'letsencrypt': {
        'reload_after': {
            'postfix',
        }, 
    },
}
