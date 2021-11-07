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
    'bind/views/external/zones',
)
def acme_zone(metadata):
    return {
        'bind': {
            'views': {
                'external': {
                    'zones': {
                        metadata.get('bind/acme_zone'): {
                            'dynamic': True,
                        },
                    },
                },
            },
        },
    }

#https://lists.isc.org/pipermail/bind-users/2006-January/061051.html
