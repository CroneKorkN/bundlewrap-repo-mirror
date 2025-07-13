defaults = {
    'apt': {
        'packages': {
            'pppoe': {},
            'dhcpcd5': {},
            'radvd': {},
        },
    },
    'nftables': {
        'nat': {
            'oifname ppp0 masquerade',
        },
    },
    'systemd': {
        'units': {
            'dhcpcd.service.d/override.conf': {
                'Service': {
                    'ReadWritePaths': {'/etc/radvd.conf'},
                },
            },
            'pppoe-isp.service': {
                'Unit': {
                    'Description': 'PPPoE Internet Connection',
                    'After': 'network.target',
                },
                'Service': {
                    'Type': 'forking',
                    'ExecStart': '/usr/sbin/pppd call isp updetach',
                    'Restart': 'on-failure',
                    'RestartSec': 5,
                },
            },
            'qdisc-ppp0.service': {
                'Unit': {
                    'Description': 'setup queuing discipline for interface ppp0',
                    'After': {
                        'pppoe-isp.service',
                        'sys-devices-virtual-net-ppp0.device',
                    },
                    'PartOf': 'pppoe-isp.service',
                    'BindsTo': 'sys-devices-virtual-net-ppp0.device',
                },
                'Service': {
                    'Type': 'oneshot',
                    'ExecStart': '/sbin/tc qdisc replace root dev ppp0 cake bandwidth 30Mbit rtt 50ms diffserv4 nat egress',
                    'RemainAfterExit': 'yes',
                },
                'Install': {
                    'WantedBy': 'multi-user.target',
                },
            }
        },
    },
}
