from ipaddress import ip_interface


defaults = {
    'apt': {
        'packages': {
            'bind9': {},
        },
    },
    'bind': {
        'zones': {},
    },
}


@metadata_reactor.provides(
    'bind/zones',
)
def dns(metadata):
    return {
        'dns': {
            metadata.get('bind/domain'): {
                'A': [
                    str(ip_interface(metadata.get('network/ipv4')).ip),
                ],
                'AAAA': [
                    str(ip_interface(metadata.get('network/ipv6')).ip),
                ]
            },
        },
    }


@metadata_reactor.provides(
    'bind/zones',
)
def collect_records(metadata):
    zones = {}
    
    for other_node in repo.nodes:
        for fqdn, records in other_node.metadata.get('dns').items():
            matching_zones = sorted(
                filter(
                    lambda potential_zone: fqdn.endswith(potential_zone),
                    metadata.get('bind/zones').keys()
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
                    zones\
                        .setdefault(zone, [])\
                        .append(
                            {'name': name, 'type': type, 'value': value}
                        )
    
    return {
        'bind': {
            'zones': zones,
        },
    }


@metadata_reactor.provides(
    'bind/zones',
)
def ns_records(metadata):
    return {
        'bind': {
            'zones': {
                zone: [
                    {'name': '@', 'type': 'NS', 'value': f"{metadata.get('bind/domain')}."},
                ] for zone in metadata.get('bind/zones').keys()
            },
        },
    }
