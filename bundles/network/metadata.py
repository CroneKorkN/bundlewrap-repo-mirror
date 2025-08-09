from ipaddress import ip_interface

defaults = {
    'network': {},
}


@metadata_reactor.provides(
    'network',
)
def dhcp(metadata):
    networks = {}

    for network_name, network_conf in metadata.get('network').items():
        _interface = ip_interface(network_conf['ipv4'])
        _ip = _interface.ip
        _network = _interface.network
        _hosts = list(_network.hosts())

        if network_conf.get('dhcp_server', False):
            networks[network_name] = {
                'dhcp_server_config': {
                    'subnet': str(_network),
                    'pool_from': str(_hosts[len(_hosts)//2]),
                    'pool_to': str(_hosts[-3]),
                    'router': str(_ip),
                    'domain-name-servers': str(_ip),
                }
            }
    return {
        'network': networks,
    }


@metadata_reactor.provides(
    'systemd/units',
    'modules-load',
)
def units(metadata):
    if node.has_bundle('systemd-networkd'):
        units = {}
        modules_load = set()

        for network_name, network_conf in metadata.get('network').items():
            interface_type = network_conf.get('type', None)

            # network

            units[f'{network_name}.network'] = {
                'Match': {
                    'Name': network_name if interface_type == 'vlan' else network_conf['interface'],
                },
                'Network': {
                    'DHCP': network_conf.get('dhcp', 'no'),
                    'IPv6AcceptRA': network_conf.get('IPv6AcceptRA', 'no'),
                    'VLAN': set(
                        other_network_name
                            for other_network_name, other_network_conf in metadata.get('network', {}).items()
                            if other_network_conf.get('type') == 'vlan' and other_network_conf['vlan_interface'] == network_name
                    )
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

            # cake WIP

            if 'cake' in network_conf:
                units[f'{network_name}.network']['CAKE'] = network_conf['cake']
                modules_load.add('sch_cake')

        return {
            'systemd': {
                'units': units,
            },
            'modules-load': modules_load,
        }
    else:
        return {}


@metadata_reactor.provides(
    'systemd/units',
)
def queuing_disciplines(metadata):
    if node.has_bundle('systemd-networkd'):
        return {
            'systemd': {
                'units': {
                    f'qdisc-{network_name}.service': {
                        'Unit': {
                            'Description': f'setup queuing discipline for interface {network_name}',
                            'Wants': 'network.target',
                            'After': 'network.target',
                            'BindsTo': 'network.target',
                        },
                        'Service': {
                            'Type': 'oneshot',
                            'ExecStart': f'/sbin/tc qdisc replace root dev {network_name} {network_conf["qdisc"]}',
                            'RemainAfterExit': 'yes',
                        },
                        'Install': {
                            'WantedBy': 'network-online.target',
                        },
                    }
                        for network_name, network_conf in metadata.get('network').items()
                        if 'qdisc' in network_conf
                },
            },
        }
    else:
        return {}
