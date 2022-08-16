directories = {
    '/etc/icingaweb2': {
#        'purge': True,
        'owner': 'www-data',
        'group': 'icingaweb2',
        'mode': '2770',
    },
    '/etc/icingaweb2/enabledModules': {
#        'purge': True,
        'owner': 'www-data',
        'group': 'icingaweb2',
        'mode': '2770',
    },
    '/etc/icingaweb2/modules': {
#        'purge': True,
        'owner': 'www-data',
        'group': 'icingaweb2',
        'mode': '2770',
    },
}

files = {
    '/etc/icingaweb2/setup.token': {
        'content': node.metadata.get('icingaweb2/setup_token'),
        'owner': 'www-data',
        'group': 'icingaweb2',
        'mode': '0660',
    },
}

symlinks = {
    '/etc/icingaweb2/enabledModules/monitoring': {
        'target': '/usr/share/icingaweb2/modules/monitoring',
        'owner': 'www-data',
        'group': 'icingaweb2',
    },
}

for name in [
    'authentication.ini',
    'config.ini',
    'groups.ini',
    'resources.ini',
    'roles.ini',
]:
    files[f'/etc/icingaweb2/{name}'] = {
        'content': repo.libs.ini.dumps(node.metadata.get(f'icingaweb2/{name}')),
        'owner': 'www-data',
        'group': 'icingaweb2',
        'mode': '0660',
    }

for name in [
    'config.ini',
    'backends.ini',
    'commandtransports.ini',
]:
    files[f'/etc/icingaweb2/modules/monitoring/{name}'] = {
        'content': repo.libs.ini.dumps(node.metadata.get(f'icingaweb2/monitoring/{name}')),
        'owner': 'www-data',
        'group': 'icingaweb2',
        'mode': '0660',
    }
