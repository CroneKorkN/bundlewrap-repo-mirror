{
    'hostname': '51.68.189.180',
    'groups': [
        'debian-13',
        'dnsserver',
        'monitored',
    ],
    'bundles': [
        'wireguard',
        'left4dead2',
    ],
    'metadata': {
        'id': 'd5080b1a-b310-48be-bd5a-02cfcecf0c90',
        'network': {
            'external': {
                'interface': 'ens3',
                'ipv4': '51.68.189.180/32',
                'gateway4': '51.68.188.1',
                'ipv6': '2001:41d0:701:1100::751a/128',
                'gateway6': '2001:41d0:701:1100::1',
                'cake': {
                    'Bandwidth': '350M',
                    'FlowIsolationMode': 'triple',
                    'PriorityQueueingPreset': 'besteffort',
                    'RTTSec': '100ms',
                },
            },
        },
        'left4dead2': {
            'vanilla': {
                'port': 27015,
                'overlays': ['vanilla'],
            },
            'tick100': {
                'port': 27016,
                'overlays': ['vanilla', 'tickrate'],
                'arguments': ['-tickrate 100'],
            },
            'server3_comp1': {
                'port': 27017,
                'overlays': ['competitive_rework'],
                'arguments': ['-tickrate 60'],
                'config': [
                    'exec server_original.cfg',
                    'sm_forcematch zonemod',
                    'hostname server3_comp1_test',
                    'motd_enabled 0',
                    'rcon_password ' + vault.decrypt('encrypt$gAAAAABpAdZhxwJ47I1AXotuZmBvyZP1ecVTt9IXFkLI28JiVS74LKs9QdgIBz-FC-iXtIHHh_GVGxxKQZprn4UrXZcvZ57kCKxfHBs3cE2JiGnbWE8_mfs=').value,
                ],
            },
        },
        'bind': {
            'master_node': 'htz.mails',
            'hostname': 'secondary.resolver.name',
        },
        # 'postfix': {
        #     'master_node': 'htz.mails',
        #     'hostname': 'mail2.sublimity.de',
        # },
        'wireguard': {
            'my_ip': '172.30.0.3/32',
            's2s': {
                'htz.mails': {
                    'allowed_ips': [
                        '10.0.0.0/24',
                        '10.0.2.0/24',
                        '10.0.9.0/24',
                        '10.0.10.0/24',
                    ],
                },
            },
        },
    },
}
