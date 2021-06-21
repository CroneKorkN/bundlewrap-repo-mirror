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

for source_string in node.metadata.get('apt/sources'):
    source = repo.libs.apt.AptSource(source_string)
    hosts\
        .setdefault(source.url.hostname, set())\
        .add(source)

for host, sources in hosts.items():
    matches = glob(join(repo.path, 'data', 'apt', 'keys', f'{host}.*'))
    if matches:
        path = f'/etc/apt/trusted.gpg.d/{basename(matches[0])}'
        files[path] = {
            'source': join(repo.path, 'data', 'apt', 'keys', basename(matches[0])),
            'content_type': 'binary',
            'triggers': {
                'action:apt_update',
            },
        }
        for source in sources:
            source.options['signed-by'] = [path]

    files[f'/etc/apt/sources.list.d/{host}.list'] = {
        'content': '\n'.join(
            str(source) for source in sorted(sources)
        ).format(
            release=node.metadata.get('os_release')
        ),
        'triggers': {
            'action:apt_update',
        },
    }
    


for package, options in node.metadata.get('apt/packages', {}).items():
    pkg_apt[package] = options
