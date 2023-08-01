from ipaddress import ip_address, ip_interface
from datetime import datetime
from hashlib import sha3_512


if node.metadata.get('bind/type') == 'master':
    master_node = node
else:
    master_node = repo.get_node(node.metadata.get('bind/master_node'))

directories[f'/var/lib/bind'] = {
    'owner': 'bind',
    'group': 'bind',
    'purge': True,
    'needs': [
        'pkg_apt:bind9',
    ],
    'needed_by': [
        'svc_systemd:bind9',
    ],
    'triggers': [
        'svc_systemd:bind9:restart',
    ],
}

directories[f'/var/cache/bind/keys'] = {
    'group': 'bind',
    'purge': True,
    'needs': [
        'pkg_apt:bind9',
    ],
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
    'needs': [
        'pkg_apt:bind9',
    ],
    'needed_by': [
        'svc_systemd:bind9',
    ],
    'triggers': [
        'svc_systemd:bind9:restart',
    ],
}

files['/etc/bind/named.conf.options'] = {
    'content_type': 'mako',
    'context': {
        'type': node.metadata.get('bind/type'),
        'slave_ips': node.metadata.get('bind/slave_ips', []),
        'master_ip': node.metadata.get('bind/master_ip', None),
    },
    'owner': 'root',
    'group': 'bind',
    'needs': [
        'pkg_apt:bind9',
    ],
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
        'type': node.metadata.get('bind/type'),
        'master_ip': node.metadata.get('bind/master_ip', None),
        'acls': {
            **master_node.metadata.get('bind/acls'),
            **{
                view_name: view_conf['match_clients']
                    for view_name, view_conf in master_node.metadata.get('bind/views').items()
            },
        },
        'views': dict(sorted(
            master_node.metadata.get('bind/views').items(),
            key=lambda e: (e[1].get('default', False), e[0]),
        )),
    },
    'owner': 'root',
    'group': 'bind',
    'needs': [
        'pkg_apt:bind9',
    ],
    'needed_by': [
        'svc_systemd:bind9',
    ],
    'triggers': [
        'svc_systemd:bind9:restart',
    ],
}

for view_name, view_conf in master_node.metadata.get('bind/views').items():
    directories[f"/var/lib/bind/{view_name}"] = {
        'owner': 'bind',
        'group': 'bind',
        'purge': True,
        'needed_by': [
            'svc_systemd:bind9',
        ],
        'triggers': [
            'svc_systemd:bind9:restart',
        ],
    }

    for zone_name, zone_conf in view_conf['zones'].items():
        files[f"/var/lib/bind/{view_name}/{zone_name}"] = {
            'source': 'db',
            'content_type': 'mako',
            'unless': f"test -f /var/lib/bind/{view_name}/{zone_name}" if zone_conf.get('allow_update', False) else 'false',
            'context': {
                'serial': datetime.now().strftime('%Y%m%d%H'),
                'records': zone_conf['records'],
                'hostname': node.metadata.get('bind/hostname'),
                'type': node.metadata.get('bind/type'),
            },
            'owner': 'bind',
            'group': 'bind',
            'needed_by': [
                'svc_systemd:bind9',
            ],
            'triggers': [
                'svc_systemd:bind9:restart',
            ],
        }


for zone_name, zone_conf in master_node.metadata.get('bind/zones').items():
    for sk in ('zsk_data', 'ksk_data'):
        data = zone_conf['dnssec'][sk]

        files[f"/var/cache/bind/keys/K{zone_name}.+008+{data['key_id']}.private"] = {
            'content_type': 'mako',
            'source': 'dnssec.private',
            'context': {
                'data': data['privkey_file'],
            },
            'group': 'bind',
            'needs': [
                'pkg_apt:bind9',
            ],
            'needed_by': [
                'svc_systemd:bind9',
            ],
            'triggers': [
                'svc_systemd:bind9:restart',
            ],
        }

        files[f"/var/cache/bind/keys/K{zone_name}.+008+{data['key_id']}.key"] = {
            'content_type': 'mako',
            'source': 'dnssec.key',
            'context': {
                'type': sk,
                'key_id': data['key_id'],
                'record': data['dnskey_record'],
            },
            'group': 'bind',
            'needs': [
                'pkg_apt:bind9',
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
        'svc_systemd:bind9:restart',
    ]
}
