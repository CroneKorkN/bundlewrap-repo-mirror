{
    'hostname': '10.0.0.15',
    'groups': [
        'debian-11',
        'raspberry-pi',
        'monitored',
    ],
    'bundles': [
        'stromzaehler',
    ],
    'metadata': {
        'id': 'dd521b8a-dc03-43f5-b29f-068f948ba3b8',
        'network': {
            'internal': {
                'interface': 'eth0',
                'ipv4': '10.0.0.15/24',
                'gateway4': '10.0.0.1',
            },
        },
        'stromzaehler': {
            'influxdb_node': 'home.server',
        },
    },
}
