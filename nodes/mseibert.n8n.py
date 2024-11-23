# https://teamvault.apps.seibert-media.net/secrets/mkqMRv/
# https://console.hetzner.cloud/projects/889138/servers/56564150

{
    #'dummy': True,
    'hostname': '159.69.178.45',
    'groups': [
        'backup',
        'debian-12',
        'monitored',
        'webserver',
    ],
    'bundles': [
        #'n8n',
        #'nodejs',
        'wireguard',
        'zfs',
    ],
    'metadata': {
        'id': '4852308e-9d36-4a0e-b533-a291e1495db3',
        'network': {
            'internal': {
                'interface': 'enp7s0',
                'ipv4': '10.0.227.3/24',
            },
            'external': {
                'interface': 'eth0',
                'ipv4': '159.69.178.45/32',
                'gateway4': '172.31.1.1',
                'ipv6': '2a01:4f8:c012:491b::1/64',
                'gateway6': 'fe80::1',
            },
        },
        'vm': {
            'cores': 2,
            'ram': 4096,
        },
        'wireguard': {
            'my_ip': '172.30.0.239/32',
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
        'zfs': {
            'pools': {
                'tank': {
                    'devices': [
                        '/var/lib/tank.img',
                    ],
                },
            },
        },
    },
}
