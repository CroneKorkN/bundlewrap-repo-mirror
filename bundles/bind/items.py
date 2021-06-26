from ipaddress import ip_address

directories[f'/var/lib/bind'] = {
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

views = [
    {
        'name': 'internal',
        'is_internal': True,
        'acl': [
            '127.0.0.1',
            '10.0.0.0/8',
            '169.254.0.0/16',
            '172.16.0.0/12',
            '192.168.0.0/16',
        ]
    },
    {
        'name': 'external', 
        'is_internal': False,
        'acl': [
            'any',
        ]
    },
]

files['/etc/bind/named.conf.local'] = {
    'content_type': 'mako',
    'context': {
        'views': views,
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

def use_record(record, records, view):
    if record['type'] in ['A', 'AAAA']:
        if view == 'external':
            # no internal addresses in external view
            if ip_address(record['value']).is_private:
                return False
        elif view == 'internal':
            # external addresses in internal view only, if no internal exists
            if ip_address(record['value']).is_global:
                for other_record in records:
                    if (
                        record['name'] == other_record['name'] and
                        record['type'] == other_record['type'] and
                        ip_address(other_record['value']).is_private
                    ):
                        return False
    return True
    
for view in views:
    directories[f"/var/lib/bind/{view['name']}"] = {
        'purge': True,
        'needed_by': [
            'svc_systemd:bind9',
        ],
        'triggers': [
            'svc_systemd:bind9:restart',
        ],
    }

    for zone, records in node.metadata.get('bind/zones').items():
        files[f"/var/lib/bind/{view['name']}/db.{zone}"] = {
            'group': 'bind',
            'source': 'db',
            'content_type': 'mako',
            'context': {
                'view': view['name'],
                'records': list(filter(
                    lambda record: use_record(record, records, view['name']),
                    records
                )),
            },
            'needs': [
                f"directory:/var/lib/bind/{view['name']}",
            ],
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
