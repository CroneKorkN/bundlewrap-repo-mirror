assert node.has_bundle('postfix')
assert node.has_bundle('postgresql')
assert node.has_bundle('letsencrypt')

directories = {
    '/etc/dovecot/ssl': {},
}

files = {
    '/etc/dovecot/dovecot.conf': {
        'content_type': 'mako',
        'context': {
            'admin_email': node.metadata.get('mailserver/admin_email'),
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
}

actions = {
    'dovecot_generate_dhparam': {
        'command': 'openssl dhparam -out /etc/dovecot/ssl/dhparam.pem 2048',
        'unless': 'test -f /etc/dovecot/ssl/dhparam.pem',
        'cascade_skip': False,
        'needs': {
            'pkg_apt:'
        },
        'triggers': {
            'svc_systemd:dovecot:restart',
        },
    },
}

svc_systemd = {
    'dovecot': {
        'needs': {
            'action:dovecot_generate_dhparam',
            'file:/etc/dovecot/dovecot.conf',
            'file:/etc/dovecot/dovecot-sql.conf',
        },
    },
}
