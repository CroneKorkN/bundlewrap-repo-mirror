assert node.has_bundle('java')

defaults = {
    'backup': {
        'paths': {
            '/var/lib/minecraft',
        },
    }
}

default_properties = {
    'broadcast-rcon-to-ops': True,
    'view-distance': 10,
    'enable-jmx-monitoring': False,
    'server-ip': None,
    'resource-pack-prompt': None,
    'rcon.port': 25251,
    'gamemode': 'survival',
    'server-port': 25250,
    'allow-nether': True,
    'enable-command-block': False,
    'enable-rcon': False,
    'sync-chunk-writes': True,
    'enable-query': False,
    'op-permission-level': 4,
    'prevent-proxy-connections': False,
    'resource-pack': None,
    'entity-broadcast-range-percentage': 100,
    'level-name': 'world',
    'rcon.password': None,
    'player-idle-timeout': 0,
    'motd': 'A Minecraft Server',
    'query.port': 25252,
    'force-gamemode': False,
    'rate-limit': 0,
    'hardcore': False,
    'white-list': False,
    'broadcast-console-to-ops': True,
    'pvp': True,
    'spawn-npcs': True,
    'spawn-animals': True,
    'snooper-enabled': True,
    'difficulty': 'easy',
    'function-permission-level': 2,
    'network-compression-threshold': 256,
    'text-filtering-config': None,
    'require-resource-pack': False,
    'spawn-monsters': True,
    'max-tick-time': 60000,
    'enforce-whitelist': False,
    'use-native-transport': True,
    'max-players': 20,
    'resource-pack-sha1': None,
    'spawn-protection': 0,
    'online-mode': True,
    'enable-status': True,
    'allow-flight': False,
    'max-world-size': 29999984,
}


@metadata_reactor.provides(
    'minecraft/servers',
)
def server_properties(metadata):
    servers = {}
    
    for name, options in metadata.get('minecraft/servers').items():
        servers[name] = {
            **default_properties,
        }

    return {
        'minecraft': {
            'servers': servers,
        },
    }


@metadata_reactor.provides(
    'systemd/units',
)
def server_unitfiles(metadata):
    units = {}
    
    for name in metadata.get('minecraft/servers'):
        units[f'minecraft-{name}.service'] = {
            'Unit': {
                'Description': f'minecraft server {name}',
                'After': 'network.target',
            },
            'Service': {
                'User': 'minecraft',
                'WorkingDirectory': f'/var/lib/minecraft/{name}',
                'ExecStart': '/usr/bin/java -Xms1024M -Xmx2560M -jar /opt/minecraft/server.jar nogui',
                'Restart': 'always',
            },
        }

    return {
        'systemd': {
            'units': units,
        },
    }
