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
                'match_clients': {
                    'our-nets',
                },
                'zones': {},
            },
            'external': {
                'default': True,
                'is_internal': False,
                'keys': {},
                'match_clients': {
                    'any',
                },
                'zones': {},
            },
        },
        'zones': set(),
    },
    'nftables': {
        'input': {
            'tcp dport 53 accept',
            'udp dport 53 accept',
        },
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
    'bind/master_ip',
    'bind/slave_ips',
)
def master_slave(metadata):
    if metadata.get('bind/master_node', None):
        return {
            'bind': {
                'type': 'slave',
                'master_ip': str(ip_interface(repo.get_node(metadata.get('bind/master_node')).metadata.get('network/external/ipv4')).ip),
            }
        }
    else:
        return {
            'bind': {
                'type': 'master',
                'slave_ips': {
                    str(ip_interface(repo.get_node(slave).metadata.get('network/external/ipv4')).ip)
                        for slave in metadata.get('bind/slaves')
                }
            }
        }


@metadata_reactor.provides(
    'dns',
)
def dns(metadata):
    return {
        'dns': {
            metadata.get('bind/hostname'): repo.libs.ip.get_a_records(metadata),
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
    if metadata.get('bind/type') == 'slave':
        return {}

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
    if metadata.get('bind/type') == 'slave':
        return {}

    return {
        'bind': {
            'views': {
                view_name: {
                    'match_clients': {
                        # allow keys from this view
                        *{
                            f'key {key}'
                                for key in view_conf['keys']
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
            },
        },
    }
