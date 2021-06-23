from json import dumps

directories['/etc/backup'] = {}

files['/etc/backup/config.json'] = {
    'content': dumps(
        {
            'server': node.metadata.get('backup/server'),
            'paths': sorted(set(node.metadata.get('backup/paths'))),
        },
        indent=4,
        sort_keys=True
    ),
}
