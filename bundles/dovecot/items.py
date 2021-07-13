assert node.has_bundle('mailserver')

users['vmail'] = {
    'home': '/var/vmail',
}

directories = {
    '/etc/dovecot': {
        'purge': True,
    },
    '/etc/dovecot/conf.d': {
        'purge': True,
        'needs': {
            'pkg_apt:dovecot-sieve',
            'pkg_apt:dovecot-managesieved',
        },
    },
    '/etc/dovecot/ssl': {},
    '/var/vmail': {
        'owner': 'vmail',
        'group': 'vmail',
    }
}

files = {
    '/etc/dovecot/dovecot.conf': {
        'content_type': 'mako',
        'context': {
            'admin_email': node.metadata.get('mailserver/admin_email'),
            'indexer_ram': node.metadata.get('dovecot/indexer_ram'),
        },
        'needs': {
            'pkg_apt:'
        },
        'triggers': {
            'svc_systemd:dovecot:restart',
        },
    },
    '/etc/dovecot/dovecot-sql.conf': {
        'content_type': 'mako',
        'context': node.metadata.get('mailserver/database'),
        'needs': {
            'pkg_apt:'
        },
        'triggers': {
            'svc_systemd:dovecot:restart',
        },
    },
    '/etc/dovecot/dhparam.pem': {
        'content_type': 'any',
    },
    '/etc/dovecot/dovecot-sql.conf': {
        'content_type': 'mako',
        'context': node.metadata.get('mailserver/database'),
        'needs': {
            'pkg_apt:'
        },
        'triggers': {
            'svc_systemd:dovecot:restart',
        },
    },
    '/var/mail/vmail/sieve/global/learn-ham.sieve': {
        'owner': 'nobody',
        'group': 'nogroup',
    },
    '/var/mail/vmail/sieve/global/learn-spam.sieve': {
        'owner': 'nobody',
        'group': 'nogroup',
    },
    '/var/mail/vmail/sieve/global/spam-global.sieve': {
        'owner': 'nobody',
        'group': 'nogroup',
    },
}

actions = {
    'dovecot_generate_dhparam': {
        'command': 'openssl dhparam -out /etc/dovecot/dhparam.pem 2048',
        'unless': 'test -f /etc/dovecot/dhparam.pem',
        'cascade_skip': False,
        'needs': {
            'pkg_apt:',
            'directory:/etc/dovecot/ssl',
        },
        'triggers': {
            'svc_systemd:dovecot:restart',
        },
    },
}

svc_systemd = {
    'dovecot': {
        'needs': {
            'action:letsencrypt_update_certificates',
            'action:dovecot_generate_dhparam',
            'file:/etc/dovecot/dovecot.conf',
            'file:/etc/dovecot/dovecot-sql.conf',
        },
    },
}

# fulltext search

directories['/usr/local/libexec/dovecot'] = {}
files['/usr/local/libexec/dovecot/decode2text.sh'] = {
    'owner': 'dovecot',
    'mode': '500',
}
