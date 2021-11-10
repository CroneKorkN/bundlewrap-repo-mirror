files = {
    '/etc/systemd/journald.conf.d/managed.conf': {
        'content': repo.libs.systemd.generate_unitfile({
                'Jorunal': node.metadata.get('systemd-journald'),
        }),
        'triggers': {
            'svc_systemd:systemd-journald:restart',
        },
    }
}

svc_systemd = {
    'systemd-journald': {},
}
