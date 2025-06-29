directories = {
    '/var/lib/mailman3': {
        'owner': 'list',
        'group': 'list',
        'needs': {
            'zfs_dataset:tank/mailman',
            'pkg_apt:mailman3-full',
        },
        'needed_by': {
            'svc_systemd:mailman3.service',
            'svc_systemd:mailman3-web.service',
        },
    },
}

files = {
    '/etc/postfix/main.cf': {
        'source': 'postfix.cf',
        'content_type': 'mako',
        'mode': '0644',
        'context': {
            'hostname': node.metadata.get('mailman/hostname'),
        },
        'needs': {
            'pkg_apt:postfix',
        },
        'triggers': {
            'svc_systemd:postfix.service:restart',
        },
    },
    '/etc/mailman3/mailman.cfg': {
        'content_type': 'mako',
        'owner': 'root',
        'group': 'list',
        'mode': '0640',
        'context': node.metadata.get('mailman'),
        'needs': {
            'pkg_apt:mailman3-full',
        },
        'triggers': {
            'svc_systemd:mailman3.service:restart',
            'svc_systemd:mailman3-web.service:restart',
        },
    },
    '/etc/mailman3/mailman-web.py': {
        'content_type': 'mako',
        'owner': 'root',
        'group': 'www-data',
        'mode': '0640',
        'context': node.metadata.get('mailman'),
        'needs': {
            'pkg_apt:mailman3-full',
        },
        'triggers': {
            'svc_systemd:mailman3.service:restart',
            'svc_systemd:mailman3-web.service:restart',
        },
    },
    '/etc/mailman3/mailman-hyperkitty.cfg': {
        'content_type': 'mako',
        'owner': 'root',
        'group': 'list',
        'mode': '0640',
        'context': node.metadata.get('mailman'),
        'needs': {
            'pkg_apt:mailman3-full',
        },
        'triggers': {
            'svc_systemd:mailman3.service:restart',
            'svc_systemd:mailman3-web.service:restart',
        },
    },
    '/etc/mailman3/uwsgi.ini': {
        'content_type': 'text',
        'owner': 'root',
        'group': 'root',
        'mode': '0644',
        'needs': {
            'pkg_apt:mailman3-full',
        },
        'triggers': {
            'svc_systemd:mailman3.service:restart',
            'svc_systemd:mailman3-web.service:restart',
        },
    },
}

svc_systemd = {
    'postfix.service': {
        'needs': {
            'pkg_apt:postfix',
        },
    },
    'mailman3.service': {
        'needs': {
            'pkg_apt:mailman3-full',
        },
    },
    'mailman3-web.service': {
        'needs': {
            'pkg_apt:mailman3-full',
        },
    },
}
