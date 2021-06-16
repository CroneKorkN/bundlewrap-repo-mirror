defaults = {
    'apt': {
        'packages': {
            'dovecot-imapd': {},
            'dovecot-pgsql': {},
            'dovecot-lmtpd': {},
#            'dovecot-sieve': {},
#            'dovecot-managesieved': {},
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
