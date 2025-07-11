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
        },
    },

}
