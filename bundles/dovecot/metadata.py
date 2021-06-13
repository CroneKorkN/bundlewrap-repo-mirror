from bundlewrap.metadata import atomic

defaults = {
    'apt': {
        'packages': {
            'dovecot-imapd': {},
            'dovecot-lmtpd': {},
            'dovecot-managesieved': {},
            'dovecot-pgsql': {},
            'dovecot-sieve': {},
        },
    },
    'letsencrypt': {
        'reload_after': {
            'dovecot',
        },
    },
    'dovecot': {
        'database': {
            'dbname': 'mailserver',
            'dbuser': 'mailserver',
        },
    },

}
