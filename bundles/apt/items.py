# TODO pin repo: https://superuser.com/a/1595920

from os.path import join, basename

directories = {
    '/etc/apt': {
        'purge': True,
        'triggers': {
            'action:apt_update',
        },
    },
    '/etc/apt/apt.conf.d': {
        # existance is expected
        'purge': True,
        'triggers': {
            'action:apt_update',
        },
    },
    '/etc/apt/keyrings': {
        # https://askubuntu.com/a/1307181
        'purge': True,
        'triggers': {
            'action:apt_update',
        },
    },
    '/etc/apt/listchanges.conf.d': {
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
    '/etc/apt/sources.list.d': {
        'purge': True,
        'triggers': {
            'action:apt_update',
        },
    },
}

files = {
    '/etc/apt/apt.conf': {
        'content': repo.libs.apt.render_apt_conf(node.metadata.get('apt/config')),
        'triggers': {
            'action:apt_update',
        },
    },
    '/etc/apt/listchanges.conf': {
        'content': repo.libs.ini.dumps(node.metadata.get('apt/list_changes')),
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

# create sources.lists and respective keyfiles

for name, config in node.metadata.get('apt/sources').items():
    # place keyfile
    keyfile_destination_path = config['options']['Signed-By']
    files[keyfile_destination_path] = {
        'source': join(repo.path, 'data', 'apt', 'keys', basename(keyfile_destination_path)),
        'content_type': 'binary',
        'triggers': {
            'action:apt_update',
        },
    }

    # place sources.list
    files[f'/etc/apt/sources.list.d/{name}.sources'] = {
        'content': repo.libs.apt.render_source(node, name),
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
