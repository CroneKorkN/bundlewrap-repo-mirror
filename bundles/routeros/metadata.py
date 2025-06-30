defaults = {}


@metadata_reactor.provides(
    'routeros/vlan_ports',
)
def routeros__(metadata):
    return {
        'routeros': {
            'vlan_ports': {
                vlan_name: {
                    'untagged': {
                        port_name
                            for port_name, port_conf in metadata.get('routeros/ports').items()
                            if vlan_name == metadata.get(f'routeros/vlan_groups/{port_conf["vlan_group"]}/untagged')
                    },
                    'tagged': {
                        port_name
                            for port_name, port_conf in metadata.get('routeros/ports').items()
                            if vlan_name in metadata.get(f'routeros/vlan_groups/{port_conf["vlan_group"]}/tagged')
                    },
                }
                        for vlan_name in metadata.get('routeros/vlans').keys()
            },
        },
    }
