from json import dumps

directories['/opt/backup'] = {}

files['/opt/backup/backup_all'] = {
    'mode': '700',
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
            'server_hostname': repo.get_node(node.metadata.get('backup/server')).metadata.get('backup-server/hostname'),
            'client_uuid': node.metadata.get('id'),
            'paths': sorted(set(node.metadata.get('backup/paths'))),
        },
        indent=4,
        sort_keys=True
    ),
}
