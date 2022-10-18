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
    'dovecot': {
        'database': {
            'dbname': 'mailserver',
            'dbuser': 'mailserver',
        },
    },
    'letsencrypt': {
        'reload_after': {
            'dovecot',
        },
    },
    'nftables': {
        'input': {
            'tcp dport {143, 993, 4190} accept',
        },
    },
    'systemd-timers': {
        'dovecot-optimize-index': {
            'command': '/usr/bin/doveadm fts optimize -A',
            'when': 'daily',
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
