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
                    'After': {
                        'pppoe-isp.service',
                        'sys-devices-virtual-net-ppp0.device',
                    },
                    'PartOf': 'pppoe-isp.service',
                    'BindsTo': 'sys-devices-virtual-net-ppp0.device',
                },
                'Service': {
                    'Type': 'oneshot',
                    'ExecStart': '/sbin/tc qdisc replace root dev ppp0 cake bandwidth 37Mbit internet besteffort triple-isolate nat egress memlimit 256mb',
                    # - no drops save
                    # - bis 37MBit keine retries bei: iperf3 --client 49.12.184.229 -t999 -i5 --bidir
                    #'ExecStart': '/sbin/tc qdisc replace root dev ppp0 cake bandwidth 37Mbit internet besteffort nat egress memlimit 256mb',
                    'RemainAfterExit': 'yes',
                },
                'Install': {
                    'WantedBy': 'multi-user.target',
                },
            }
        },
    },
}
