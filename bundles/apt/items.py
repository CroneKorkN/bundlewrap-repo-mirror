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
    '/etc/apt/trusted.gpg.d': {
        'purge': True,
        'triggers': {
            'action:apt_update',
        },
    },
    '/etc/apt/preferences.d': {
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

# group sources by apt server hostname

hosts = {}

for source_string in node.metadata.get('apt/sources'):
    source = repo.libs.apt.AptSource(source_string)
    hosts\
        .setdefault(source.url.hostname, set())\
        .add(source)

# create sources lists and keyfiles

for host, sources in hosts.items():
    keyfile = basename(glob(join(repo.path, 'data', 'apt', 'keys', f'{host}.*'))[0])
    destination_path = f'/etc/apt/trusted.gpg.d/{keyfile}'

    for source in sources:
        source.options['signed-by'] = [destination_path]

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
    
    files[destination_path] = {
        'source': join(repo.path, 'data', 'apt', 'keys', keyfile),
        'content_type': 'binary',
        'triggers': {
            'action:apt_update',
        },
    }

# create backport pinnings

for package, options in node.metadata.get('apt/packages', {}).items():    
    pkg_apt[package] = options

    if pkg_apt[package].pop('backports', False):
        files[f'/etc/apt/preferences.d/{package}'] = {
            'content': '\n'.join([
                f"Package: {package}",
                f"Pin: release a={node.metadata.get('os_release')}-backports",
                f"Pin-Priority: 900",
            ]),
            'needed_by': [
                f'pkg_apt:{package}',
            ],
            'triggers': {
                'action:apt_update',
            },
        }
