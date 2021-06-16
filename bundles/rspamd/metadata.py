defaults = {
    'apt': {
        'packages': {
            'clamav': {},
            'clamav-daemon': {},
            'clamav-freshclam': {},
            'clamav-unofficial-sigs': {}, 
            'rspamd': {},
        },
    },
    'rspamd': {
        'web_password': repo.vault.password_for(node.name + ' rspamd web password'),
        'ignore_spam_check_for_ips': [],
    },
}
