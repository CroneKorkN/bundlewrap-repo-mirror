defaults = {
    'apt': {
        'packages': {
            'dovecot-imapd':        {},
            'dovecot-pgsql':        {},
            'dovecot-lmtpd':        {},
            # spam filtering
            'dovecot-sieve':        {},
            'dovecot-managesieved': {},
            # fulltext search
            'dovecot-fts-xapian':   {}, # buster-backports
            'poppler-utils':        {}, # pdftotext
            'catdoc':               {}, # catdoc, catppt, xls2csv
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

@metadata_reactor.provides(
    'dovecot/indexer_ram',
)
def indexer_ram(metadata):
    return {
        'dovecot': {
            'indexer_ram': str(metadata.get('vm/ram')//2)+ 'M',
        },
    }
