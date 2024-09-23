from ipaddress import ip_interface

hashable = repo.libs.hashable.hashable


defaults = {
    'apt': {
        'packages': {
            'kea-dhcp4-server': {},
        },
    },
    'kea': {
        'Dhcp4': {
            'interfaces-config': {
                'interfaces': set(),
            },
            'lease-database': {
                'type': 'memfile',
                'lfc-interval': 3600
            },
            'subnet4': set(),
            'loggers': set([
                hashable({
                    'name': 'kea-dhcp4',
                    'output_options': [
                        {
                            'output': 'syslog',
                        }
                    ],
                    'severity': 'INFO',
                }),
            ]),
        },
    },
}


@metadata_reactor.provides(
    'kea',
)
def subnets(metadata):
    subnet4 = set()
    interfaces = set()

    for network_name, network_conf in metadata.get('network').items():
        dhcp_server_config = network_conf.get('dhcp_server_config', None)

        if dhcp_server_config:
            subnet4.add(hashable({
                'subnet': dhcp_server_config['subnet'],
                'pools': [
                    {
                        'pool': f'{dhcp_server_config['pool_from']} - {dhcp_server_config['pool_to']}',
                    },
                ],
                'option-data': [
                    {
                        'name': 'routers',
                        'data': dhcp_server_config['router'],
                    },
                    {
                        'name': 'domain-name-servers',
                        'data': '10.0.10.2',
                    },
                ],
            }))
            interfaces.add(network_conf.get('interface', network_name))

    return {
        'kea': {
            'Dhcp4': {
                'interfaces-config': {
                    'interfaces': interfaces,
                },
                'subnet4': subnet4,
            },
        },
    }
