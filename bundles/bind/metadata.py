from ipaddress import ip_interface
from json import dumps
h = repo.libs.hashable.hashable
repo.libs.bind.repo = repo

defaults = {
    'apt': {
        'packages': {
            'bind9': {},
        },
    },
    'bind': {
        'slaves': {},
        'acls': {
            'our-nets': {
                '127.0.0.1',
                '10.0.0.0/8',
                '169.254.0.0/16',
                '172.16.0.0/12',
                '192.168.0.0/16',
            }
        },
        'views': {
            'internal': {
                'is_internal': True,
                'keys': {},
                'acl': {
                    'our-nets',
                },
                'zones': {},
            },
            'external': {
                'default': True,
                'is_internal': False,
                'keys': {},
                'acl': {
                    'any',
                },
                'zones': {},
            },
        },
        'zones': set(),
    },
    'telegraf': {
        'config': {
            'inputs': {
                'bind': [{
                    'urls': ['http://localhost:8053/xml/v3'],
                    'gather_memory_contexts': False,
                    'gather_views': True,
                }],
            },
        },
    },
}


@metadata_reactor.provides(
    'bind/type',
)
def type(metadata):
    return {
        'bind': {
            'type': 'slave' if metadata.get('bind/master_node', None) else 'master',
        }
    }


@metadata_reactor.provides(
    'dns',
)
def dns(metadata):
    return {
        'dns': {
            metadata.get('bind/hostname'): repo.libs.dns.get_a_records(metadata),
        }
    }


@metadata_reactor.provides(
    'bind/views',
)
def collect_records(metadata):
    if metadata.get('bind/type') == 'slave':
        return {}
    
    views = {}

    for view_name, view_conf in metadata.get('bind/views').items():
        for other_node in repo.nodes:
            for fqdn, records in other_node.metadata.get('dns', {}).items():
                matching_zones = sorted(
                    filter(
                        lambda potential_zone: fqdn.endswith(potential_zone),
                        metadata.get('bind/zones')
                    ),
                    key=len,
                )
                if matching_zones:
                    zone = matching_zones[-1]
                else:
                    continue

                name = fqdn[0:-len(zone) - 1]

                for type, values in records.items():                    
                    for value in values:
                        if repo.libs.bind.record_matches_view(value, type, name, zone, view_name, metadata):
                            views\
                                .setdefault(view_name, {})\
                                .setdefault('zones', {})\
                                .setdefault(zone, {})\
                                .setdefault('records', set())\
                                .add(
                                    h({'name': name, 'type': type, 'value': value})
                                )
    
    return {
        'bind': {
            'views': views,
        },
    }


@metadata_reactor.provides(
    'bind/views',
)
def ns_records(metadata):
    if metadata.get('bind/type') == 'slave':
        return {}

    nameservers = [
        node.metadata.get('bind/hostname'),
        *[
            repo.get_node(slave).metadata.get('bind/hostname')
                for slave in node.metadata.get('bind/slaves')
        ]
    ]
    return {
        'bind': {
            'views': {
                view_name: {
                    'zones': {
                        zone_name: {
                            'records': {
                                # FIXME: bw currently cant handle lists of dicts :(
                                h({'name': '@', 'type': 'NS', 'value': f"{nameserver}."})
                                    for nameserver in nameservers
                            } 
                        }
                        for zone_name, zone_conf in view_conf['zones'].items()
                    }
                }
                    for view_name, view_conf in metadata.get('bind/views').items()
            },
        },
    }


@metadata_reactor.provides(
    'bind/slaves',
)
def slaves(metadata):
    if metadata.get('bind/type') == 'slave':
        return {}
    
    return {
        'bind': {
            'slaves': [
                other_node.name
                    for other_node in repo.nodes
                    if other_node.has_bundle('bind') and other_node.metadata.get('bind/master_node', None) == node.name
            ],
        },
    }


@metadata_reactor.provides(
    'bind/views',
)
def generate_keys(metadata):
    return {
        'bind': {
            'views': {
                view_name: {
                    'keys': {
                        key: {
                            'token':repo.libs.hmac.hmac_sha512(
                                key,
                                str(repo.vault.random_bytes_as_base64_for(
                                    f"{metadata.get('id')} bind key {key}",
                                    length=32,
                                )),
                            )
                        }
                            for key in view_conf['keys']
                    }
                }
                    for view_name, view_conf in metadata.get('bind/views').items()
            }
        }
    }


@metadata_reactor.provides(
    'bind/views',
)
def generate_acl_entries_for_keys(metadata):
    return {
        'bind': {
            'views': {
                view_name: {
                    'acl': {
                        # allow keys from this view
                        *{
                            f'key {view_name}.{zone_name}'
                                for zone_name, zone_conf in view_conf['zones'].items()
                                if zone_conf.get('key', False)
                        },
                        # reject keys from other views
                        *{
                            f'! key {key}'
                                for other_view_name, other_view_conf in metadata.get('bind/views').items()
                                if other_view_name != view_name
                                for key in other_view_conf.get('keys', [])
                        }
                    }
                }
                    for view_name, view_conf in metadata.get('bind/views').items()
                    if not view_conf.get('default')
            },
        },
    }
