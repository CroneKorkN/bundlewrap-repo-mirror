assert node.has_bundle('java')

defaults = {
    'systemd': {
        'units': {
            'minecraft.service': {
                'Unit': {
                    'Description': 'minecraft',
                    'After': 'network.target',
                },
                'Service': {
                    'User': 'minecraft',
                    'WorkingDirectory': '/opt/minecraft',
                    'ExecStart': '/usr/bin/java -Xms1024M -Xmx2560M -jar /opt/minecraft/server.jar nogui',
                    'Restart': 'always',
                },
            },
        },
    },
}
