users = {
    'minecraft': {},
}

directories = {
    '/opt/minecraft': {
        'owner': 'minecraft',
    },
    '/var/lib/minecraft': {
        'owner': 'minecraft',
    },
}

downloads = {
    '/opt/minecraft/server.jar': {
        'url': node.metadata.get('minecraft/download'),
        'sha256': node.metadata.get('minecraft/sha256'),
        'needs': {
            'directory:/opt/minecraft',
        },
    }
}


for name, properties in node.metadata.get('minecraft/servers').items():
    directories[f'/var/lib/minecraft/{name}'] = {
        'owner': 'minecraft',
    }

    files[f'/var/lib/minecraft/{name}/eula.txt'] = {
        'content': 'eula=true',
        'owner': 'minecraft',
        'needed_by': {
            f'svc_systemd:minecraft-{name}'
        },
        'triggers': {
            f'svc_systemd:minecraft-{name}:restart'
        },
    }

    translations = {True: 'true', False: 'false', None: ''}
    files[f'/var/lib/minecraft/{name}/server.properties'] = {
        'content': '\n'.join(
            f'{key}={translations.get(value, value)}'
                for key, value in properties.items()
        ),
        'owner': 'minecraft',
        'needed_by': {
            f'svc_systemd:minecraft-{name}'
        },
        'triggers': {
            f'svc_systemd:minecraft-{name}:restart'
        },
    }

    svc_systemd[f'minecraft-{name}'] = {}
