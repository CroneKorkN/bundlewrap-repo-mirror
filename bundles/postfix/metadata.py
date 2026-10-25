from ipaddress import ip_interface


defaults = {
    'apt': {
        'packages': {
            'postfix': {},
            'postfix-pgsql': {},
            'acl': {}, #setfacl
        }
    },
    'backup': {
        'paths': {
            '/var/vmail',
        },
    },
    'postfix': {
        'mynetworks': set(),
    },
    'grafana_rows': {
        'postfix_queue',
    },
    'letsencrypt': {
        'reload_after': {
            'postfix',
        },
    },
    'nftables': {
        'input': {
            'tcp dport {25, 465, 587} accept',
        },
    },
    'telegraf': {
        'inputs': {
            'postfix': {
                'default': {},
            },
        },
    },
}


@metadata_reactor.provides(
    'postfix/mynetworks',
)
def mynetworks(metadata):
    # the nodes relaying through this one, see bundle postfix-relay; through wireguard they come from either address
    return {
        'postfix': {
            'mynetworks': {
                ip
                    for other_node in repo.nodes
                    if not other_node.dummy
                    and other_node.has_bundle('postfix-relay')
                    and not other_node.has_bundle('postfix')
                    for ip in {
                        repo.libs.ip.internal_ip(other_node.metadata),
                        *(
                            {str(ip_interface(other_node.metadata.get('wireguard/my_ip')).ip)}
                            if other_node.metadata.get('wireguard/my_ip', None) else set()
                        ),
                    }
            },
        },
    }
