file_attributes = {
    'owner': 'opendkim',
    'group': 'opendkim',
    'mode': '700',
    'triggers': [
        'svc_systemd:opendkim:restart',
    ],
}

groups['opendkim'] = {}
users['opendkim'] = {}

directories = {
    '/etc/opendkim': {
        **file_attributes,
        'purge' : True,
    },
    '/etc/opendkim/keys': {
        **file_attributes,
        'purge' : True,
    },
}

files = {
    '/etc/opendkim.conf': {
        **file_attributes,
    },
    '/etc/defaults/opendkim': {
        # https://metadata.ftp-master.debian.org/changelogs//main/o/opendkim/testing_opendkim.NEWS
        'delete': True,
    },
    '/etc/opendkim/key_table': {
        'content_type': 'mako',
        'context': {
            'domains': node.metadata.get('opendkim/domains'),
        },
        **file_attributes,
    },
    '/etc/opendkim/signing_table': {
        'content_type': 'mako',
        'context': {
            'domains': node.metadata.get('opendkim/domains'),
        },
        **file_attributes,
    },
}

for domain in node.metadata.get('opendkim/domains'):
    directories[f'/etc/opendkim/keys/{domain}'] = {
        **file_attributes,
        'purge': True,
    }
    files[f'/etc/opendkim/keys/{domain}/mail.private'] = {
        **file_attributes,
        'content_type': 'any',
    }
    files[f'/etc/opendkim/keys/{domain}/mail.txt'] = {
        **file_attributes,
        'content_type': 'any',
    }
    actions[f'generate_{domain}_dkim_key'] = {
        'command': (
            f'sudo --user opendkim'
            f' opendkim-genkey'
            f' --selector=mail'
            f' --directory=/etc/opendkim/keys/{domain}'
            f' --domain={domain}'
        ),
        'unless': f'test -f /etc/opendkim/keys/{domain}/mail.private',
        'needs': [
            'svc_systemd:opendkim',
            f'directory:/etc/opendkim/keys/{domain}',
        ],
        'triggers': [
            'svc_systemd:opendkim:restart',
        ],
    }

svc_systemd['opendkim'] = {
    'needs': [
        'pkg_apt:opendkim',
        'file:/etc/opendkim.conf',
        'file:/etc/opendkim/key_table',
        'file:/etc/opendkim/signing_table',
    ],
}
