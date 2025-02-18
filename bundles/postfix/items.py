assert node.has_bundle('mailserver')

file_options = {
    'needs': [
        'pkg_apt:postfix',
    ],
    'needed_by': [
        'svc_systemd:postfix',
    ],
    'triggers': [
        'svc_systemd:postfix:restart',
    ],
}

files = {
    '/etc/postfix/main.cf': {
        'content_type': 'mako',
        'context': {
            'hostname': node.metadata.get('mailserver/hostname'),
            'debug': node.metadata.get('mailserver/debug')
        },
        **file_options,
    },
    '/etc/postfix/master.cf': {
        **file_options,
    },
    '/etc/postfix/virtual_mailbox_domains.cf': {
        'content_type': 'mako',
        'context': node.metadata.get('mailserver/database'),
        **file_options,
    },
    '/etc/postfix/virtual_mailbox_maps.cf': {
        'content_type': 'mako',
        'context': node.metadata.get('mailserver/database'),
        **file_options,
    },
    '/etc/postfix/virtual_alias_maps.cf': {
        'content_type': 'mako',
        'context': node.metadata.get('mailserver/database'),
        **file_options,
    },
}

svc_systemd['postfix'] = {
    'needs': [
        'postgres_db:mailserver',
    ],
}

actions['test_postfix_config'] = {
    'command': 'false',
    'unless': "postconf check | grep -v 'symlink leaves directory' | wc -l | grep -q '^0$'",
    'needs': [
        'svc_systemd:postfix',
    ],
}
actions['test_virtual_mailbox_domains'] = {
    'command': 'false',
    'unless': "postmap -q example.com pgsql:/etc/postfix/virtual_mailbox_domains.cf | grep -q '^example.com$'",
    'needs': [
        'svc_systemd:postfix',
        'action:mailserver_update_test_pw',
    ],
}
actions['test_virtual_mailbox_maps'] = {
    'command': 'false',
    'unless': "postmap -q bw_test_user@example.com pgsql:/etc/postfix/virtual_mailbox_maps.cf | grep -q '^bw_test_user@example.com$'",
    'needs': [
        'svc_systemd:postfix',
        'action:mailserver_update_test_pw',
    ],
}
actions['test_virtual_alias_maps'] = {
    'command': 'false',
    'unless': "postmap -q bw_test_alias@example.com pgsql:/etc/postfix/virtual_alias_maps.cf | grep -q '^somewhere@example.com$'",
    'needs': [
        'svc_systemd:postfix',
        'action:mailserver_update_test_pw',
    ],
}

if node.has_bundle('telegraf'):
    actions['postfix_setfacl_telegraf'] = {
        'command': 'setfacl -Rm g:telegraf:rX /var/spool/postfix',
        'unless': 'getfacl -a /var/spool/postfix | grep -q "^group:telegraf:r-x$"',
        'needs': [
            'pkg_apt:acl',
            'svc_systemd:postfix',
            'svc_systemd:postfix:reload',
            'svc_systemd:postfix:restart',
        ],
    }
    actions['postfix_setfacl_default_telegraf'] = {
        'command': 'setfacl -dm g:telegraf:rX /var/spool/postfix',
        'unless': 'getfacl -d /var/spool/postfix | grep -q "^group:telegraf:r-x$"',
        'needs': [
            'pkg_apt:acl',
            'svc_systemd:postfix',
            'svc_systemd:postfix:reload',
            'svc_systemd:postfix:restart',
        ],
    }
