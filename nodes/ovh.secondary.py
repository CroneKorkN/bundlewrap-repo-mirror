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
            'servers': {
                'vanilla': {
                    'port': 27015,
                    'overlays': ['vanilla'],
                    'config': [
                        'sv_consistency 0',
                    ],
                },
                'tick100': {
                    'port': 27016,
                    'arguments': ['-tickrate 100'],
                    'overlays': ['tickrate', 'vanilla', 'workshop_maps'],
                    'config': [
                        'exec server_tickrate.cfg',
                        'sv_minupdaterate 101',
                        'sv_maxupdaterate 101',
                        'sv_mincmdrate 101',
                        'sv_maxcmdrate 101',
                        'sv_consistency 0',
                    ],
                },
                'tick100_maps': {
                    'port': 27017,
                    'arguments': ['-tickrate 100'],
                    'overlays': ['tickrate', 'vanilla', 'workshop_maps'],
                    'config': [
                        'exec server_tickrate.cfg',
                        'sv_minupdaterate 101',
                        'sv_maxupdaterate 101',
                        'sv_mincmdrate 101',
                        'sv_maxcmdrate 101',
                        'sv_consistency 0',
                    ],
                },
                'vanilla_maps': {
                    'port': 27018,
                    'overlays': ['vanilla', 'workshop_maps'],
                    'config': [
                        'sv_consistency 0',
                    ],
                },
                'tick60_maps': {
                    'port': 27019,
                    'arguments': ['-tickrate 60'],
                    'overlays': ['tickrate', 'vanilla', 'workshop_maps'],
                    'config': [
                        'exec server_tickrate.cfg',
                        'sv_minupdaterate 101',
                        'sv_maxupdaterate 101',
                        'sv_mincmdrate 101',
                        'sv_maxcmdrate 101',
                        'sv_consistency 0',
                    ],
                },
                'zonemod': {
                    'port': 27020,
                    'arguments': ['-tickrate 60'],
                    'overlays': ['competitive_rework'],
                    'config': [
                        'exec server_competitive_rework.cfg',
                        'sm_forcematch zonemod',
                    ],
                },
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
