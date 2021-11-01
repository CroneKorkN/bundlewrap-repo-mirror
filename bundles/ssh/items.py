if not node.metadata.get('FIXME_dont_touch_sshd', False):
    # on debian bullseye raspberry images, starting the systemd ssh
    # daemon seems to collide with an existing sysv daemon
    files['/etc/ssh/sshd_config'] = {
        'triggers': [
            'svc_systemd:ssh:restart'
        ],
    }

    svc_systemd['ssh'] = {
        'needs': [
            'tag:ssh_users',
        ],
    }
