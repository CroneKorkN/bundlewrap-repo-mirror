h = repo.libs.hashable.hashable


@metadata_reactor.provides(
    'bind/acme_hostname',
)
def acme_hostname(metadata):
    return {
        'bind': {
            'acme_hostname': 'acme.'+ metadata.get('bind/hostname'),
        },
    }


@metadata_reactor.provides(
    'bind/zones',
)
def acme_records(metadata):
    if metadata.get('bind/type') == 'slave':
        return {}

    return {
        'bind': {
            'zones': {
                zone: {
                    'records': {
                        # FIXME: bw currently cant handle lists of dicts :(
                        h({ 
                            'name': f"_acme-challenge{'.' if name else ''}{name}",
                            'type': 'CNAME',
                            'value': metadata.get('bind/acme_hostname'),
                        })
                            for name in {
                                record['name'] if record['name'] != '@' else ''
                                    for record in conf['records']
                                    if f"{record['name']}.{zone}" in metadata.get('letsencrypt/domains')
                            }
                    }
                }
                    for zone, conf in metadata.get('bind/zones').items()
                    if zone != metadata.get('bind/acme_hostname')
            },
        },
    }



@metadata_reactor.provides(
    'bind/zones',
)
def acme_zone(metadata):
    if metadata.get('bind/type') == 'slave':
        return {}

    return {
        'bind': {
            'zones': {
                metadata.get('bind/hostname'): {
                    'keys': ['acme'],
                    'records': set(),
                },
            },
        },
    }
