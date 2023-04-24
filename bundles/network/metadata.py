from ipaddress import ip_interface

defaults = {
    'network': {},
}


@metadata_reactor.provides(
    'network/internal_interface',
)
def internal_interface(metadata):
    if (
        metadata.get('network/interfaces/internal', None)
        and not metadata.get('network/internal_interface', None)
    ):
        return {
            'network': {
                'internal_interface': 'internal',
            }
        }
    else:
        return {}


@metadata_reactor.provides(
    'network/internal_ipv4',
)
def internal_ipv4(metadata):
    if (
        metadata.get('network/internal_interface', None)
        and not metadata.get('network/internal_ipv4', None)
    ):
        internal_interface = metadata.get('network/internal_interface', None)
        return {
            'network': {
                'internal_ipv4': metadata.get(f'network/interfaces/{internal_interface}/ipv4'),
            }
        }
    else:
        return {}


@metadata_reactor.provides(
    'systemd/units',
)
def units(metadata):
    units = {}

    for name, conf in metadata.get('network/interfaces').items():
        units[f'{name}.network'] = {
            'Match': {
                'Name': conf['match'],
            },
            'Network': {
                'DHCP': conf.get('dhcp', 'no'),
                'IPv6AcceptRA': conf.get('dhcp', 'no'),
            }
        }

        for i in [4, 6]:
            if conf.get(f'ipv{i}', None):
                units[f'{name}.network'].update({
                    f'Address#ipv{i}': {
                        'Address': conf[f'ipv{i}'],
                    },
                })
                if f'gateway{i}' in conf:
                    units[f'{name}.network'].update({
                        f'Route#ipv{i}': {
                            'Gateway': conf[f'gateway{i}'],
                            'GatewayOnlink': 'yes',
                        }
                    })


    return {
        'systemd': {
            'units': units,
        }
    }
