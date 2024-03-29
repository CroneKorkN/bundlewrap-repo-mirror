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
        'needs': [
            'pkg_apt:dovecot-sieve',
            'pkg_apt:dovecot-managesieved',
        ]
    },
    '/etc/dovecot/ssl': {},
    '/var/vmail': {
        'owner': 'vmail',
        'group': 'vmail',
    },
    '/var/vmail/index': {
        'owner': 'vmail',
        'group': 'vmail',
    },
    '/var/vmail/sieve': {
        'owner': 'vmail',
        'group': 'vmail',
    },
    '/var/vmail/sieve/global': {
        'owner': 'vmail',
        'group': 'vmail',
    },
    '/var/vmail/sieve/bin': {
        'owner': 'vmail',
        'group': 'vmail',
    },
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
    '/var/vmail/sieve/global/spam-to-folder.sieve': {
        'owner': 'vmail',
        'group': 'vmail',
        'triggers': {
            'svc_systemd:dovecot:restart',
        },
    },
    '/var/vmail/sieve/global/learn-ham.sieve': {
        'owner': 'vmail',
        'group': 'vmail',
        'triggers': {
            'svc_systemd:dovecot:restart',
        },
    },
    '/var/vmail/sieve/bin/learn-ham.sh': {
        'owner': 'vmail',
        'group': 'vmail',
        'mode': '550',
    },
    '/var/vmail/sieve/global/learn-spam.sieve': {
        'owner': 'vmail',
        'group': 'vmail',
        'triggers': {
            'svc_systemd:dovecot:restart',
        },
    },
    # /usr/local/libexec/dovecot?
    # /usr/lib/dovecot/sieve-pipe?
    '/var/vmail/sieve/bin/learn-spam.sh': {
        'owner': 'vmail',
        'group': 'vmail',
        'mode': '550',
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
