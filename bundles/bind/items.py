from ipaddress import ip_address, ip_interface
from datetime import datetime

if node.metadata.get('bind/type') == 'master':
    zones = node.metadata.get('bind/zones')
    master_ip = None
    slave_ips = [
        ip_interface(repo.get_node(slave).metadata.get('network/external/ipv4')).ip
            for slave in node.metadata.get('bind/slaves')
    ]
else:
    zones = repo.get_node(node.metadata.get('bind/master_node')).metadata.get('bind/zones')
    master_ip = ip_interface(repo.get_node(node.metadata.get('bind/master_node')).metadata.get('network/external/ipv4')).ip
    slave_ips = []

directories[f'/var/lib/bind'] = {
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
        'slave_ips': sorted(slave_ips),
        'master_ip': master_ip,
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
        'master_ip': master_ip,
        'views': dict(sorted(
            node.metadata.get('bind/views').items(),
            key=lambda e: (e[1].get('default', False), e[0]),
        )),
        'zones': zones,
        'hostname': node.metadata.get('bind/hostname'),
        'keys': node.metadata.get('bind/keys'),
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

def record_matches_view(record, records, view):
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
    
for view_name, view_conf in node.metadata.get('bind/views').items():
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

    for zone, conf in zones.items():
        if view_name not in conf.get('views', ['internal', 'external']):
            continue
        
        records = conf['records']
        unique_records = [
            dict(record_tuple)
                for record_tuple in set(
                    tuple(record.items()) for record in records
                )
        ]
        
        files[f"/var/lib/bind/{view_name}/db.{zone}"] = {
            'owner': 'bind',
            'group': 'bind',
            'needs': [
                f"directory:/var/lib/bind/{view_name}",
            ],
            'needed_by': [
                'svc_systemd:bind9',
            ],
            'triggers': [
                'svc_systemd:bind9:restart',
            ],
        }
        if True or node.metadata.get('bind/type') == 'master': #FIXME: slave doesnt get updated if db doesnt get rewritten on each apply
            files[f"/var/lib/bind/{view_name}/db.{zone}"].update({
                'source': 'db',
                'content_type': 'mako',
                'unless': f"test -f /var/lib/bind/{view_name}/db.{zone}" if conf.get('dynamic', False) else 'false',
                'context': {
                    'view': view_name,
                    'serial': datetime.now().strftime('%Y%m%d%H'),
                    'records': list(filter(
                        lambda record: record_matches_view(record, records, view_name),
                        unique_records
                    )),
                    'hostname': node.metadata.get('bind/hostname'),
                    'type': node.metadata.get('bind/type'),
                    'keys': node.metadata.get('bind/keys'),
                },
            })

svc_systemd['bind9'] = {}

actions['named-checkconf'] = {
    'command': 'named-checkconf -z',
    'unless': 'named-checkconf -z',
    'needs': [
        'svc_systemd:bind9',
        'svc_systemd:bind9:restart',
    ]
}
