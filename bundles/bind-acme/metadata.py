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
                for other_node in repo.nodes
                for domain in other_node.metadata.get('letsencrypt/domains', {}).keys()
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
                    'dynamic': True,
                    'records': set(),
                    'views': ['external'],
                },
            },
        },
    }
