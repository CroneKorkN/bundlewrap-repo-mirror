# Git-Hash for Icinga1: b63bb0ef52bf213715e567c81e3ed097024e61af

from json import load
from os.path import join

ICINGA_PLUGINS = {
}

ENABLED_FEATURES = [
    'ido-pgsql',
    'notification',
]
for feature in ENABLED_FEATURES:
    symlinks[f'/etc/icinga2/features-enabled/{feature}.conf'] = {
        'target': f'/etc/icinga2/features-available/{feature}.conf',
        'owner': 'nagios',
        'group': 'nagios',
        'needs': [
            'pkg_apt:icinga2-ido-pgsql',
        ],
        'triggers': [
            'svc_systemd:icinga2:restart',
        ],
    }

svc_systemd = {
    'icinga2': {
        'needs': [
            'pkg_apt:icinga2-ido-pgsql',
            'svc_systemd:postgresql',
        ],
    },
}

directories = {
    '/etc/icinga2/features-enabled': {
        'purge': True,
    },
}

files = {
    '/etc/icinga2/features-available/ido-pgsql.conf': {
        'source': 'ido-pgsql.conf',
        'content_type': 'mako',
        'context': {
            'db_password': node.metadata.get('postgresql/roles/icinga2/password')
        },
        'owner': 'nagios',
        'group': 'nagios',
        'needs': [
            'pkg_apt:icinga2-ido-pgsql',
        ],
    },
}
