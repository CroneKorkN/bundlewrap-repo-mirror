files = {
    '/etc/systemd/journald.conf.d/managed.conf': {
        'content': repo.libs.systemd.generate_unitfile({
                'Journal': node.metadata.get('systemd-journald'),
        }),
        'triggers': {
            'svc_systemd:systemd-journald:restart',
        },
    }
}

svc_systemd = {
    'systemd-journald': {},
}
