assert node.has_bundle('gcloud')
assert node.has_bundle('gocryptfs')
assert node.has_bundle('gocryptfs-inspect')
assert node.has_bundle('systemd')

from json import dumps

directories['/opt/archive'] = {}
directories['/etc/archive'] = {}

files['/etc/archive/archive.json'] = {
    'content': dumps(
        {
            'node_name': node.name,
            **node.metadata.get('archive'),
        },
        indent=4,
        sort_keys=True
    ),
}

files['/opt/archive/archive'] = {
    'content_type': 'mako',
    'mode': '700',
    'context': {
        'paths': node.metadata.get('archive/paths'),
        'bucket': node.metadata.get('gcloud/bucket'),
        'processes': 4,
        'threads': 4,
    },
    'needs': [
        'bundle:gcloud',
    ],
}
    
files['/opt/archive/get_file'] = {
    'mode': '700',
}

files['/opt/archive/validate_file'] = {
    'mode': '700',
}
