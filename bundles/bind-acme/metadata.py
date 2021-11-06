@metadata_reactor.provides(
    'dns',
)
def acme_records(metadata):
    domains = set()
    
    for other_node in repo.nodes:
        for domain, conf in other_node.metadata.get('letsencrypt/domains', {}).items():
            domains.add(domain)
            domains.update(conf.get('aliases', []))
    
    return {
        'dns': {
            f'_acme-challenge.{domain}': {
                'CNAME': {f"{domain}.{metadata.get('bind/acme_zone')}."},
            }
                for domain in domains
        }
    }


@metadata_reactor.provides(
    'bind/zones',
)
def acme_zone(metadata):
    return {
        'bind': {
            'zones': {
                metadata.get('bind/acme_zone'): {
                    'dynamic': True,
                    'views': ['external'],
                    'records': set(),
                },
            },
        },
    }
