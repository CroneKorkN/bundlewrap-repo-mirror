from os.path import join
from urllib.parse import urlparse
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

hosts = {}

for source in node.metadata.get('apt/sources'):
    host = repo.libs.apt.AptSource(source).url.hostname
    hosts\
        .setdefault(host, set())\
        .add(source)

for host, sources in hosts.items():
    files[f'/etc/apt/sources.list.d/{host}.list'] = {
        'content': '\n'.join(sorted(sources)).format(
            release=node.metadata.get('os_release')
        ),
        'triggers': {
            'action:apt_update',
        },
    }
    
    matches = glob(join(repo.path, 'data', 'apt', 'keys', f'{host}.*'))
    if matches:
        files[f'/etc/apt/trusted.gpg.d/{basename(matches[0])}'] = {
            'source': join(repo.path, 'data', 'apt', 'keys', basename(matches[0])),
            'content_type': 'binary',
            'triggers': {
                'action:apt_update',
            },
        }


for package, options in node.metadata.get('apt/packages', {}).items():
    pkg_apt[package] = options
