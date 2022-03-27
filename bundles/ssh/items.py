if not node.metadata.get('FIXME_dont_touch_sshd', False):
    # on debian bullseye raspberry images, starting the systemd ssh
    # daemon seems to collide with an existing sysv daemon
    directories = {
        '/etc/ssh': {
            'purge': True,
            'mode': '0755',
        }
    }
    
    files = {
        '/etc/ssh/moduli': {
            'content_type': 'any',
        },
        '/etc/ssh/ssh_config': {
            'triggers': [
                'svc_systemd:ssh:restart'
            ],
        },
        '/etc/ssh/ssh_config': {
            'content_type': 'mako',
            'context': {
            },
            'triggers': [
                'svc_systemd:ssh:restart'
            ],
        },
        '/etc/ssh/sshd_config': {
            'content_type': 'mako',
            'context': {
                'users': sorted(node.metadata.get('ssh/allow_users')),
            },
            'triggers': [
                'svc_systemd:ssh:restart'
            ],
        },
        '/etc/ssh/ssh_host_ed25519_key': {
            'content': node.metadata.get('ssh/host_key/private') + '\n',
            'mode': '0600',
            'triggers': [
                'svc_systemd:ssh:restart'
            ],
        },
        '/etc/ssh/ssh_host_ed25519_key.pub': {
            'content': node.metadata.get('ssh/host_key/public') + '\n',
            'mode': '0644',
            'triggers': [
                'svc_systemd:ssh:restart'
            ],
        },
        '/etc/ssh/ssh_known_hosts': {
            'content': '\n'.join(
                repo.libs.ssh.known_hosts_entry_for(other_node)
                    for other_node in sorted(repo.nodes)
                    if other_node != node
                    and other_node.has_bundle('ssh')
            ) + '\n',
        },
    }

    svc_systemd['ssh'] = {
        'needs': [
            'tag:ssh_users',
        ],
    }
