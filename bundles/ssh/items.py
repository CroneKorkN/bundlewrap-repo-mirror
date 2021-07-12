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
