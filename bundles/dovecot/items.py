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
            'config_version': node.metadata.get('dovecot/config_version'),
            'storage_version': node.metadata.get('dovecot/storage_version'),
            'maildir': node.metadata.get('mailserver/maildir'),
            'hostname': node.metadata.get('mailserver/hostname'),
            'db_host': node.metadata.get('mailserver/database/host'),
            'db_name': node.metadata.get('mailserver/database/name'),
            'db_user': node.metadata.get('mailserver/database/user'),
            'db_password': node.metadata.get('mailserver/database/password'),
            'indexer_cores': node.metadata.get('vm/cores'),
            'indexer_ram': node.metadata.get('vm/ram')//2,
        },
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
        },
    },
}

# fulltext search

directories['/usr/local/libexec/dovecot'] = {}
files['/usr/local/libexec/dovecot/decode2text.sh'] = {
    'owner': 'dovecot',
    'mode': '500',
}
