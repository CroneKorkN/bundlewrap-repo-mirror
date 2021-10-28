{
    'hostname': '10.0.0.15',
    'groups': [
        'debian-11',
        'raspberry-pi',
        'monitored',
    ],
    'bundles': [
        'stromzaehler',
        'wpa-supplicant',
    ],
    'metadata': {
        'id': 'dd521b8a-dc03-43f5-b29f-068f948ba3b8',
        'network': {
            'internal': {
                'interface': 'eth0',
                'ipv4': '10.0.0.15/24',
                'gateway4': '10.0.0.1',
            },
            'wlan': {
                'interface': 'wlan0',
                'ipv4': '10.0.0.16/24',
                'gateway4': '10.0.0.1',
            },
        },
        'stromzaehler': {
            'influxdb_node': 'home.server',
        },
        'wpa-supplicant': {
            'interface': 'wlan0',
            'ssid': 'wingl',
            'password': 'encrypt$gAAAAABhewMmeeBVKljTX3W3nb3vXaMtcJe2xSHpmCliG_JwPvxR6sgWbAokFpiV4RFL32wqxMZSd9KYPk0zV36WmqLiCWfWXg==',
        },
    },
}
