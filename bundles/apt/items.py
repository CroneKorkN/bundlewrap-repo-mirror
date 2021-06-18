from glob import glob
from os.path import join, basename

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
    
    matches = glob(join(repo.path, 'data', 'apt', 'keys', f'{name}.*'))
    if matches:
        assert len(matches) == 1
        files[f'/etc/apt/trusted.gpg.d/{basename(matches[0])}'] = {
            'source': matches[0],
            'content_type': 'binary',
            'triggers': {
                'action:apt_update',
            },
        }


for package, options in node.metadata.get('apt/packages', {}).items():
    pkg_apt[package] = options
