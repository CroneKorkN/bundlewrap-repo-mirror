{
    'hostname': '141.95.32.8',
    'groups': [
        'backup',
        'debian-13',
        'left4me',
        'monitored',
        'webserver',
    ],
    'bundles': [
        'wireguard',
    ],
    'metadata': {
        'id': '14d2abc-3855-4bb7-99e2-d4e3eb0344dd',
        'vm': {
            'cores': 4,    # 4 physical, 8 with HT
            'threads': 8,
        },
        'network': {
            'external': {
                'interface': 'enp3s0f0',
                'ipv4': '141.95.32.8/24',
                'gateway4': '141.95.32.254',
                'ipv6': '2001:41d0:700:5508::1/128',
                'gateway6': '2001:41d0:700:55ff:ff:ff:ff:ff',
                'cake': {
                    'Bandwidth': '450M',
                    'FlowIsolationMode': 'triple',
                    'PriorityQueueingPreset': 'besteffort',
                    'RTTSec': '100ms',
                },
            },
        },
        'wireguard': {
            'my_ip': '172.30.0.5/32',
            's2s': {
                'htz.mails': {
                    'allowed_ips': [
                        '10.0.0.0/16',
                    ],
                },
            },
        },
        'left4me': {
            'domain': 'left4.me',
            # Both HT siblings of physical core 0 (cpu0+cpu4 per
            # /sys/devices/system/cpu/cpu0/topology/thread_siblings_list).
            # Keeps system work off the physical cores running game ticks.
            'system_cpus': {0, 4},
        },
    },
}
