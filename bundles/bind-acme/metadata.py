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
    'dns',
)
def acme_records(metadata):
    if metadata.get('bind/type') == 'slave':
        return {}

    return {
        'dns': {
            f'_acme-challenge.{domain}': {
                'CNAME': {f"{domain}.{metadata.get('bind/acme_hostname')}."},
            }
                for domain in node.metadata.get('letsencrypt/domains')
        }
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
                metadata.get('bind/acme_hostname'): {
                    'keys': ['acme'],
                    'records': set(),
                },
            },
        },
    }
