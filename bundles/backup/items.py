from json import dumps

directories['/etc/backup'] = {}

files['/etc/backup/config.json'] = {
    'content': dumps(
        {
            'server_hostname': repo.get_node(node.metadata.get('backup/server')).metadata.get('backup-server/hostname'),
            'paths': sorted(set(node.metadata.get('backup/paths'))),
        },
        indent=4,
        sort_keys=True
    ),
}
