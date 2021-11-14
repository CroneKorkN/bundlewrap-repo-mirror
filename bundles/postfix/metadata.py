defaults = {
    'apt': {
        'packages': {
            'postfix': {},
            'postfix-pgsql': {},
            'acl': {}, #setfacl
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
    'grafana_rows': {
        'postfix_queue',
    },
}
