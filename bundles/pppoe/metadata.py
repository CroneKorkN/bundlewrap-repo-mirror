defaults = {
    'apt': {
        'packages': {
            'pppoe': {},
        },
    },
    'nftables': {
        'nat': {
            'oifname ppp0 masquerade',
        },
    },
    'systemd': {
        'units': {
            'pppoe-isp.service': {
                'Unit': {
                    'Description': 'PPPoE Internet Connection',
                    'After': 'network.target',
                },
                'Service': {
                    'Type': 'forking',
                    'ExecStart': '/usr/sbin/pppd call isp',
                    'Restart': 'on-failure',
                    'RestartSec': 5,
                },
            },
            'qdisc-ppp0.service': {
                'Unit': {
                    'Description': 'setup queuing discipline for interface ppp0',
                    'After': 'sys-devices-virtual-net-ppp0.device',
                    'BindsTo': 'sys-devices-virtual-net-ppp0.device',
                },
                'Service': {
                    'Type': 'oneshot',
                    'ExecStart': '/sbin/tc qdisc replace root dev ppp0 cake bandwidth 30Mbit rtt 50ms diffserv4 nat egress',
                    'RemainAfterExit': 'yes',
                },
                'Install': {
                    'WantedBy': 'network-online.target',
                },
            }
        },
    },
}
