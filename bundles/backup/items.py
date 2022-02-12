from json import dumps


backup_node = repo.get_node(node.metadata.get('backup/server'))

directories['/opt/backup'] = {}

files['/opt/backup/backup_all'] = {
    'mode': '700',
    'content_type': 'mako',
    'context': {
        'wol_command': backup_node.metadata.get('wol-sleeper/wake_command', False),
    },
}
files['/opt/backup/backup_path'] = {
    'mode': '700',
}
files['/opt/backup/backup_path_via_zfs'] = {
    'mode': '700',
}
files['/opt/backup/backup_path_via_rsync'] = {
    'mode': '700',
}

directories['/etc/backup'] = {}

files['/etc/backup/config.json'] = {
    'content': dumps(
        {
            'server_hostname': backup_node.metadata.get('backup-server/hostname'),
            'client_uuid': node.metadata.get('id'),
            'paths': sorted(set(node.metadata.get('backup/paths'))),
        },
        indent=4,
        sort_keys=True
    ),
}
