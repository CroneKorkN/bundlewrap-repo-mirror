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
    'grafana_rows': {
        'postfix_queue',
    },
    'letsencrypt': {
        'reload_after': {
            'postfix',
        },
    },
    'nftables': {
        'input': {
            'tcp dport {25, 465, 587} accept',
        },
    },
    'telegraf': {
        'inputs': {
            'postfix': {
                'default': {},
            },
        },
    },
}
