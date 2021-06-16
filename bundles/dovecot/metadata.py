defaults = {
    'apt': {
        'packages': {
            'dovecot-imapd':      {},
            'dovecot-pgsql':      {},
            'dovecot-lmtpd':      {},
#            'dovecot-sieve': {},
#            'dovecot-managesieved': {},
            # fulltext search
            'dovecot-fts-xapian': {}, # buster-backports
            'poppler-utils':      {}, # pdftotext
            'catdoc':             {}, # catdoc, catppt, xls2csv
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
