from ipaddress import ip_interface

defaults = {
    'network': {},
}


@metadata_reactor.provides(
    'systemd/units',
)
def units(metadata):
    units = {}

    for network_name, network_conf in metadata.get('network').items():
        interface_type = network_conf.get('type', None)

        # network

        units[f'{network_name}.network'] = {
            'Match': {
                'Name': network_name if interface_type == 'vlan' else network_conf['interface'],
            },
            'Network': {
                'DHCP': network_conf.get('dhcp', 'no'),
                'IPv6AcceptRA': network_conf.get('dhcp', 'no'),
                'VLAN': set(network_conf.get('vlans', set()))
            }
        }

        # type

        if interface_type:
            units[f'{network_name}.network']['Match']['Type'] = interface_type

        # ips

        for i in [4, 6]:
            if network_conf.get(f'ipv{i}', None):
                units[f'{network_name}.network'].update({
                    f'Address#ipv{i}': {
                        'Address': network_conf[f'ipv{i}'],
                    },
                })
                if f'gateway{i}' in network_conf:
                    units[f'{network_name}.network'].update({
                        f'Route#ipv{i}': {
                            'Gateway': network_conf[f'gateway{i}'],
                            'GatewayOnlink': 'yes',
                        }
                    })

        # as vlan

        if interface_type == 'vlan':
            units[f"{network_name}.netdev"] = {
                'NetDev': {
                    'Name': network_name,
                    'Kind': 'vlan',
                },
                'VLAN': {
                    'Id': network_conf['id'],
                }
            }

    return {
        'systemd': {
            'units': units,
        }
    }
