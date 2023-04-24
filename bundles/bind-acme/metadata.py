from ipaddress import ip_interface


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
    'bind/acls/acme',
    'bind/views/external/keys/acme',
    'bind/views/external/zones',
)
def acme_zone(metadata):
    allowed_ips = {
        *{
            str(ip_interface(other_node.metadata.get('network/internal_ipv4')).ip)
                for other_node in repo.nodes
                if other_node.metadata.get('letsencrypt/domains', {})
        },
        *{
            str(ip_interface(other_node.metadata.get('wireguard/my_ip')).ip)
                for other_node in repo.nodes
                if other_node.has_bundle('wireguard')
        },
    }

    return {
        'bind': {
            'acls': {
                'acme': {
                    'key acme',
                    '!{ !{' + ' '.join(f'{ip};' for ip in sorted(allowed_ips)) + '}; any;}',
                },
            },
            'views': {
                'external': {
                    'keys': {
                        'acme': {},
                    },
                    'zones': {
                        metadata.get('bind/acme_zone'): {
                            'allow_update': {
                                'acme',
                            },
                        },
                    },
                },
            },
        },
    }

#https://lists.isc.org/pipermail/bind-users/2006-January/061051.html
