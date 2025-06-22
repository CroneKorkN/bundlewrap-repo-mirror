# https://teamvault.apps.seibert-media.net/secrets/mkqMRv/
# https://console.hetzner.cloud/projects/889138/servers/46578341

{
    'hostname': '168.119.250.114',
    'groups': [
        #'backup',
        'debian-12',
        #'monitored',
        'webserver',
    ],
    'bundles': [
        #'wireguard',
        'mariadb',
        'php',
        'yourls',
        'zfs',
    ],
    'metadata': {
        'id': '52efcd47-edd8-426c-aead-c492553d14f9',
        'network': {
            'internal': {
                'interface': 'ens10',
                'ipv4': '10.0.227.4/24',
            },
            'external': {
                'interface': 'eth0',
                'ipv4': '168.119.250.114/32',
                'gateway4': '172.31.1.1',
                'ipv6': '2a01:4f8:c013:e321::2/64',
                'gateway6': 'fe80::1',
            },
        },
        'yourls': {
            'hostname': "direkt.oranienschule.de",
            'cookiekey': "!decrypt:encrypt$gAAAAABoRvmcUs3t7PREllyeN--jBqs0XYewMHW16GWC-ikLzsDSe02YKGycOlgXuHU4hzKbNjGMEutpFXRLk9Zji6bbpy4GdyE6vStfwd8ZT0obAyoqBPwI47LwUlDSFMS51y5j8rG5",
            'version': "1.10.1",
            'users': {
                'mseibert': "!decrypt:encrypt$gAAAAABoRwtOcslyRY9ahkmtVI8QbXgJhyE3nuk04eakFDKl-4OZViiRvjtQW3Uwqki1aFeAS-syzr0Ug5sZM_zNelNahjZyzW1k47Xg9GltGNn_zp-uUII=",
            },
        },
        # FIXME:
        'overwrite_nameservers': [
            '8.8.8.8',
        ],
        'vm': {
            'cores': 2,
            'ram': 4096,
        },
        'zfs': {
            'pools': {
                'tank': {
                    'devices': [
                        '/var/lib/zfs_file',
                    ],
                },
            },
        },
    },
}
