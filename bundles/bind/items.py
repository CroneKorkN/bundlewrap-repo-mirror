directories['/var/lib/bind'] = {
    'purge': True,
    'needed_by': [
        'svc_systemd:bind9',
    ],
    'triggers': [
        'svc_systemd:bind9:restart',
    ],
}

files['/etc/default/bind9'] = {
    'source': 'defaults',
    'needed_by': [
        'svc_systemd:bind9',
    ],
    'triggers': [
        'svc_systemd:bind9:restart',
    ],
}

files['/etc/bind/named.conf'] = {
    'owner': 'root',
    'group': 'bind',
    'needed_by': [
        'svc_systemd:bind9',
    ],
    'triggers': [
        'svc_systemd:bind9:restart',
    ],
}
files['/etc/bind/named.conf.options'] = {
    'owner': 'root',
    'group': 'bind',
    'needed_by': [
        'svc_systemd:bind9',
    ],
    'triggers': [
        'svc_systemd:bind9:restart',
    ],
}
files['/etc/bind/named.conf.local'] = {
    'content_type': 'mako',
    'context': {
        'zones': sorted(node.metadata.get('bind/zones')),
    },
    'owner': 'root',
    'group': 'bind',
    'needed_by': [
        'svc_systemd:bind9',
    ],
    'triggers': [
        'svc_systemd:bind9:restart',
    ],
}

for zone, records in node.metadata.get('bind/zones').items():
    files[f'/var/lib/bind/db.{zone}'] = {
        'group': 'bind',
        'source': 'db',
        'content_type': 'mako',
        'context': {
            'records': records,
        },
        'needed_by': [
            'svc_systemd:bind9',
        ],
        'triggers': [
            'svc_systemd:bind9:restart',
        ],
    }

svc_systemd['bind9'] = {}

actions['named-checkconf'] = {
    'command': 'named-checkconf -z',
    'unless': 'named-checkconf -z',
    'needs': [
        'svc_systemd:bind9',
    ]
}
