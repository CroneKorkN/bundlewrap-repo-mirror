from json import dumps


directories['/opt/backup-server'] = {}

files['/opt/backup-server/prune-snapshots'] = {
    'mode': '755',
}

directories['/etc/backup-server'] = {}

files['/etc/backup-server/retention.json'] = {
    'content': dumps(node.metadata.get('backup-server/retention'), indent=4, sort_keys=True),
}
