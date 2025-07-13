from ipaddress import ip_interface


# on debian bullseye raspberry images, starting the systemd ssh
# daemon seems to collide with an existing sysv daemon
dont_touch_sshd = node.metadata.get('FIXME_dont_touch_sshd', False)

directories = {
    '/etc/ssh': {
        'purge': True,
        'mode': '0755',
        'skip': dont_touch_sshd,
    }
}

files = {
    '/etc/ssh/moduli': {
        'content_type': 'any',
        'skip': dont_touch_sshd,
    },
    '/etc/ssh/ssh_config': {
        'triggers': [
            'svc_systemd:ssh:restart'
        ],
        'skip': dont_touch_sshd,
    },
    '/etc/ssh/ssh_config': {
        'content_type': 'mako',
        'context': {
            'multiplex_incoming': node.metadata.get('ssh/multiplex_incoming'),
            'multiplex_hosts': set(
                str(ip_interface(other_node.metadata.get('network/internal/ipv4')).ip)
                    for other_node in repo.nodes
                    if other_node.has_bundle('ssh')
                    and other_node.metadata.get('network/internal/ipv4', None)
                    and other_node.metadata.get('ssh/multiplex_incoming')
            ),
        },
        'triggers': [
            'svc_systemd:ssh:restart'
        ],
        'skip': dont_touch_sshd,
    },
    '/etc/ssh/sshd_config': {
        'content_type': 'mako',
        'context': {
            'users': sorted(node.metadata.get('ssh/allow_users')),
        },
        'triggers': [
            'svc_systemd:ssh:restart'
        ],
        'skip': dont_touch_sshd,
    },
    '/etc/ssh/ssh_host_managed_key': {
        'content': node.metadata.get('ssh/host_key/private') + '\n',
        'mode': '0600',
        'triggers': [
            'svc_systemd:ssh:restart'
        ],
    },
    '/etc/ssh/ssh_host_managed_key.pub': {
        'content': node.metadata.get('ssh/host_key/public') + '\n',
        'mode': '0644',
        'triggers': [
            'svc_systemd:ssh:restart'
        ],
    },
    '/etc/ssh/ssh_known_hosts': {
        'content': '\n'.join(sorted(node.metadata.get('ssh/known_hosts'))) + '\n',
    },
}

svc_systemd['ssh'] = {
    'needs': [
        'tag:ssh_users',
    ],
    'skip': dont_touch_sshd,
}
