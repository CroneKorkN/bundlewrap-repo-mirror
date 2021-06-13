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

for package, options in node.metadata.get('apt/packages', {}).items():
    pkg_apt[package] = options
