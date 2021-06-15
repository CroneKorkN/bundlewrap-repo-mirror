assert node.has_bundle('mailserver')

file_options = {
    'triggers': [
        'svc_systemd:postfix:restart',
    ],
    'needed_by': [
        'svc_systemd:postfix',
    ],
}

files = {
    '/etc/postfix/main.cf': {
        'content_type': 'mako',
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
