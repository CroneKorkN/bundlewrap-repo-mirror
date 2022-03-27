# Git-Hash for Icinga1: b63bb0ef52bf213715e567c81e3ed097024e61af

directories = {
    '/etc/icinga2': {
        'purge': True,
        'owner': 'nagios',
    },
    '/etc/icinga2/conf.d': {
        'purge': True,
        'owner': 'nagios',
    },
    '/etc/icinga2/hosts.d': {
        'purge': True,
        'owner': 'nagios',
    },
    '/etc/icinga2/features.d': {
        'purge': True,
        'owner': 'nagios',
    },
}

files = {
    '/etc/icinga2/icinga2.conf': {
        'owner': 'nagios',
    },
    '/etc/icinga2/constants.conf': {
        'owner': 'nagios',
        'context': {
            'hostname': node.metadata.get('icinga2/hostname')
        },
    },
    '/etc/icinga2/conf.d/templates.conf': {
        'source': 'conf.d/templates.conf',
        'owner': 'nagios',
    },
    '/etc/icinga2/features/ido-pgsql.conf': {
        'source': 'features/ido-pgsql.conf',
        'content_type': 'mako',
        'owner': 'nagios',
        'context': {
            'db_password': node.metadata.get('postgresql/roles/icinga2/password')
        },
        'needs': [
            'pkg_apt:icinga2-ido-pgsql',
        ],
    },
}

for other_node in repo.nodes:
    files[f'/etc/icinga2/hosts.d/{other_node.name}.conf'] = {
        'content_type': 'mako',
        'source': 'hosts.d/host.conf',
        'owner': 'nagios',
        'context': {
            'host_name': other_node.name,
            'host_settings': {},
            'services': other_node.metadata.get('monitoring', {}),
        },
    }

svc_systemd = {
    'icinga2': {
        'needs': [
            'pkg_apt:icinga2-ido-pgsql',
            'svc_systemd:postgresql',
        ],
    },
}
