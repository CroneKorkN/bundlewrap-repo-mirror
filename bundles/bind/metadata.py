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
def collect_records(metadata):
    zones = metadata.get('bind/zones')
    
    for other_node in repo.nodes:
        print(other_node.name)
        for fqdn, records in other_node.metadata.get('dns').items():
            matching_zones = sorted(
                filter(
                    lambda potential_zone: fqdn.endswith(potential_zone),
                    zones
                ),
                key=len,
            )
            
            if matching_zones:
                zone = matching_zones[0]
            else:
                continue

            name = fqdn[0:-len(zone) - 1]

            for type, values in records.items():
                for value in values:
                    zones\
                        .setdefault(zone, [])\
                        .append(
                            (name, type, value)
                        )
    
    return {
        'bind': {
            'zones': zones,
        },
    }
