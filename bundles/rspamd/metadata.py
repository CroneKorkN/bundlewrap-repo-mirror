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
    'nginx': {
        'vhosts': {
            'rspamd.sublimity.de': {
                'content': 'nginx/proxy_pass.conf',
                'context': {
                    'target': 'http://localhost:11334',
                },
            },
        },
    },
    'rspamd': {
        'web_password': repo.vault.password_for(node.name + ' rspamd web password'),
        'ignore_spam_check_for_ips': [],
    },
}
