{
    'hostname': '141.95.32.8',
    'groups': [
        'debian-13',
        'monitored',
    ],
    'bundles': [
        'wireguard',
    ],
    'metadata': {
        'id': '14d2abc-3855-4bb7-99e2-d4e3eb0344dd',
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
    },
}
