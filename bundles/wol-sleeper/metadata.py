@metadata_reactor.provides(
    'apt/packages/ethtool',
    'systemd/units/enable-wol',
    'systemd/services/enable-wol.service',
)
def systemd(metadata):
    interfaces = set(
        conf['interface']
            for conf in metadata.get('network').values()
            if conf.get('wol', False)
    )
    
    if not interfaces:
        return {}
    
    return {
        'apt': {
            'packages': {
                'ethtool': {},
            },
        },
        'systemd': {
            'units': {
                'enable-wol.service': {
                    'Unit': {
                        'After': 'network.target',
                    },
                    'Service': {
                        'Type': 'oneshot',
                        'RemainAfterExit': 'yes',
                        'ExecStart': set(
                            f"ethtool -s {interface} wol g"
                                for interface in interfaces
                        ),
                    },
                    'Install': {
                        'WantedBy': 'multi-user.target',
                    },
                },
            },
            'services': {
                'enable-wol.service': {},
            },
        },
    }
