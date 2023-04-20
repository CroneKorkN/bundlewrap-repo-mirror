# TODO pin repo: https://superuser.com/a/1595920

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
    '/usr/lib/nagios/plugins/check_apt_upgradable': {
        'mode': '0755',
    },
}

actions = {
    'apt_update': {
        'command': 'apt-get update -o APT::Update::Error-Mode=any',
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
        .setdefault(source.url.hostname, list())\
        .append(source)

# create sources lists and keyfiles

for host, sources in hosts.items():
    keyfile = basename(glob(join(repo.path, 'data', 'apt', 'keys', f'{host}.*'))[0])
    destination_path = f'/etc/apt/trusted.gpg.d/{keyfile}'

    for source in sources:
        source.options['signed-by'] = [destination_path]

    files[f'/etc/apt/sources.list.d/{host}.list'] = {
        'content': '\n'.join(sorted(set(
            str(source).format(
                codename=node.metadata.get('os_codename'),
                version=node.os_version[0], # WIP crystal
            )
                for source in sources
        ))),
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
                f"Pin: release a={node.metadata.get('os_codename')}-backports",
                f"Pin-Priority: 900",
            ]),
            'needed_by': [
                f'pkg_apt:{package}',
            ],
            'triggers': {
                'action:apt_update',
            },
        }

# unattended upgrades
#
# unattended-upgrades.service: delays shutdown if necessary
# apt-daily.timer: performs apt update
# apt-daily-upgrade.timer: performs apt upgrade

files['/etc/apt/apt.conf.d/20auto-upgrades'] = {}
files['/etc/apt/apt.conf.d/50unattended-upgrades'] = {}
svc_systemd['unattended-upgrades.service'] = {
    'needs': [
        'pkg_apt:unattended-upgrades',
    ],
}
svc_systemd['apt-daily.timer'] = {
    'needs': [
        'pkg_apt:unattended-upgrades',
    ],
}
svc_systemd['apt-daily-upgrade.timer'] = {
    'needs': [
        'pkg_apt:unattended-upgrades',
    ],
}
