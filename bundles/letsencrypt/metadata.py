from ipaddress import ip_interface

defaults = {
    'apt': {
        'packages': {
            'dehydrated': {},
        },
    },
    'letsencrypt': {
        'domains': {
            # 'example.com': {'alias1.example.com', 'alias2.example.com'},
        },
    },
    'pacman': {
        'packages': {
            'dehydrated': {},
        },
    },
}


@metadata_reactor.provides(
    'systemd-timers/letsencrypt',
    'mirror/certs',
)
def renew(metadata):
    delegated_node = metadata.get('letsencrypt/delegate_to_node', False)
    
    if delegated_node:
        delegated_ip = ip_interface(repo.get_node(delegated_node).metadata.get('network/internal/ipv4')).ip
        return {
            'mirror': {
                'certs': {
                    'from': f"{delegated_ip}:/var/lib/dehydrated/certs",
                    'to': '/var/lib/dehydrated',
                },
            },
        }
    else:
        return {
            'systemd-timers': {
                'letsencrypt': {
                    'command': '/bin/bash -c "/usr/bin/dehydrated --cron --accept-terms --challenge http-01 && /usr/bin/dehydrated --cleanup"',
                    'when': 'daily',
                },
            },
        }


@metadata_reactor.provides(
    'letsencrypt/domains'
)
def delegated_domains(metadata):
    return {
        'letsencrypt': {
            'domains': {
                domain: set()
                    for other_node in repo.nodes
                    if other_node.has_bundle('letsencrypt')
                        and other_node.metadata.get('letsencrypt/delegate_to_node', None) == node.name
                    for domain in other_node.metadata.get('letsencrypt/domains').keys()
            },
        },
    }
