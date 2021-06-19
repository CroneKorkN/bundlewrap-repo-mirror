from os.path import join

directories = {
    '/etc/apt/sources.list.d': {
        'purge': True,
        'triggers': {
            'action:apt_update',
        },
    },
} 

files = {
    '/etc/apt/sources.list': {
        'content': '# managed'
    },
}

actions = {
    'apt_update': {
        'command': 'apt-get update',
        'needed_by': {
            'pkg_apt:',
        },
        'triggered': True,
        'cascade_skip': False,
    },
}

for name, content in node.metadata.get('apt/sources').items():
    files[f'/etc/apt/sources.list.d/{name}.list'] = {
        'content': content.format(
            release=node.metadata.get('os_release')
        ),
        'triggers': {
            'action:apt_update',
        },
    }

for key in node.metadata.get('apt/keys'):
    files[f'/etc/apt/trusted.gpg.d/{key}'] = {
        'source': join(repo.path, 'data', 'apt', 'keys', key),
        'content_type': 'binary',
        'triggers': {
            'action:apt_update',
        },
    }


for package, options in node.metadata.get('apt/packages', {}).items():
    pkg_apt[package] = options
