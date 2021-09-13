users = {
    'minecraft': {},
}

directories = {
    '/opt/minecraft': {
        'owner': 'minecraft',
    },
}

downloads = {
    '/opt/minecraft/server.jar': {
        'url': node.metadata.get('minecraft/download'),
        'sha256': node.metadata.get('minecraft/sha256'),
    }
}

files = {
    '/opt/minecraft/eula.txt': {
        'content': 'eula=true',
    }
}

svc_systemd = {
    'minecraft': {
        'needs': {
            'file:/opt/minecraft/eula.txt',
            'download:/opt/minecraft/server.jar',
        },
    },
}
