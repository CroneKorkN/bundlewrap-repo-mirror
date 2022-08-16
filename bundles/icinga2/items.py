from ipaddress import ip_interface

directories = {
    '/etc/icinga2': {
       'purge': True,
        'owner': 'nagios',
        'group': 'nagios',
        'mode': '0750',
        'triggers': [
            'svc_systemd:icinga2.service:restart',
        ],
    },
    '/etc/icinga2/conf.d': {
        'purge': True,
        'owner': 'nagios',
        'group': 'nagios',
        'mode': '0750',
        'triggers': [
            'svc_systemd:icinga2.service:restart',
        ],
    },
    '/etc/icinga2/hosts.d': {
        'purge': True,
        'owner': 'nagios',
        'group': 'nagios',
        'mode': '0750',
        'triggers': [
            'svc_systemd:icinga2.service:restart',
        ],
    },
    '/etc/icinga2/features.d': {
        'purge': True,
        'owner': 'nagios',
        'group': 'nagios',
        'mode': '0750',
        'triggers': [
            'svc_systemd:icinga2.service:restart',
        ],
    },
    '/etc/icinga2/scripts': {
        'owner': 'nagios',
        'group': 'nagios',
        'mode': '0750',
        'triggers': [
            'svc_systemd:icinga2.service:restart',
        ],
    },
}

files = {
    '/etc/icinga2/icinga2.conf': {
        'owner': 'nagios',
        'group': 'nagios',
        'mode': '0640',
        'triggers': [
            'svc_systemd:icinga2.service:restart',
        ],
    },
    '/etc/icinga2/constants.conf': {
        'content_type': 'mako',
        'owner': 'nagios',
        'group': 'nagios',
        'mode': '0640',
        'context': {
            'hostname': node.metadata.get('hostname')
        },
        'triggers': [
            'svc_systemd:icinga2.service:restart',
        ],
    },
    '/etc/icinga2/zones.conf': {
        'content_type': 'mako',
        'context': {
            'hostname': node.metadata.get('icinga2/hostname')
        },
        'owner': 'nagios',
        'group': 'nagios',
        'mode': '0640',
        'triggers': [
            'svc_systemd:icinga2.service:restart',
        ],
    },
    '/etc/icinga2/conf.d/api-users.conf': {
        'source': 'conf.d/api-users.conf',
        'content_type': 'mako',
        'owner': 'nagios',
        'group': 'nagios',
        'mode': '0640',
        'context': {
            'users': node.metadata.get('icinga2/api_users'),
        },
        'triggers': [
            'svc_systemd:icinga2.service:restart',
        ],
    },
    '/etc/icinga2/conf.d/app.conf': {
        'source': 'conf.d/app.conf',
        'content_type': 'mako',
        'owner': 'nagios',
        'group': 'nagios',
        'mode': '0640',
        'triggers': [
            'svc_systemd:icinga2.service:restart',
        ],
    },
    '/etc/icinga2/conf.d/commands.conf': {
        'source': 'conf.d/commands.conf',
        'content_type': 'mako',
        'owner': 'nagios',
        'group': 'nagios',
        'mode': '0640',
        'triggers': [
            'svc_systemd:icinga2.service:restart',
        ],
    },
    '/etc/icinga2/conf.d/groups.conf': {
        'source': 'conf.d/groups.conf',
        'content_type': 'mako',
        'owner': 'nagios',
        'group': 'nagios',
        'mode': '0640',
        'triggers': [
            'svc_systemd:icinga2.service:restart',
        ],
    },
    '/etc/icinga2/conf.d/notifications.conf': {
        'source': 'conf.d/notifications.conf',
        'content_type': 'mako',
        'owner': 'nagios',
        'group': 'nagios',
        'mode': '0640',
        'triggers': [
            'svc_systemd:icinga2.service:restart',
        ],
    },
    '/etc/icinga2/conf.d/templates.conf': {
        'source': 'conf.d/templates.conf',
        'content_type': 'mako',
        'owner': 'nagios',
        'group': 'nagios',
        'mode': '0640',
        'triggers': [
            'svc_systemd:icinga2.service:restart',
        ],
    },
    '/etc/icinga2/conf.d/timeperiods.conf': {
        'source': 'conf.d/timeperiods.conf',
        'content_type': 'mako',
        'owner': 'nagios',
        'group': 'nagios',
        'mode': '0640',
        'triggers': [
            'svc_systemd:icinga2.service:restart',
        ],
    },
    '/etc/icinga2/features.d/ido-pgsql.conf': {
        'source': 'features/ido-pgsql.conf',
        'content_type': 'mako',
        'owner': 'nagios',
        'context': {
            'db_password': node.metadata.get('postgresql/roles/icinga2/password')
        },
        'triggers': [
            'svc_systemd:icinga2.service:restart',
        ],
    },
    '/etc/icinga2/features.d/syslog.conf': {
        'source': 'features/syslog.conf',
        'owner': 'nagios',
        'triggers': [
            'svc_systemd:icinga2.service:restart',
        ],
    },
    '/etc/icinga2/features.d/notification.conf': {
        'source': 'features/notification.conf',
        'owner': 'nagios',
        'triggers': [
            'svc_systemd:icinga2.service:restart',
        ],
    },
    '/etc/icinga2/features.d/checker.conf': {
        'source': 'features/checker.conf',
        'owner': 'nagios',
        'triggers': [
            'svc_systemd:icinga2.service:restart',
        ],
    },
    '/etc/icinga2/features.d/api.conf': {
        'source': 'features/api.conf',
        'owner': 'nagios',
        'triggers': [
            'svc_systemd:icinga2.service:restart',
        ],
    },
}

for other_node in repo.nodes:
    if other_node.dummy:
        continue

    files[f'/etc/icinga2/hosts.d/{other_node.name}.conf'] = {
        'content_type': 'mako',
        'source': 'hosts.d/host.conf',
        'owner': 'nagios',
        'context': {
            'host_name': other_node.name,
            'host_settings': {
                'address': str(ip_interface(other_node.metadata.get('network/internal/ipv4', None) or other_node.metadata.get('wireguard/my_ip')).ip),
            },
            'services': other_node.metadata.get('monitoring', {}),
        },
        'triggers': [
            'svc_systemd:icinga2.service:restart',
        ],
    }

svc_systemd = {
    'icinga2.service': {
        'needs': [
            'pkg_apt:icinga2-ido-pgsql',
            'svc_systemd:postgresql',
        ],
    },
}
