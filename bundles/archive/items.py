assert node.has_bundle('gcloud')
assert node.has_bundle('gocryptfs')
assert node.has_bundle('systemd')

files['/opt/archive'] = {
    'content_type': 'mako',
    'mode': '700',
    'context': {
        'dirs': node.metadata.get('archive'),
        'bucket': node.metadata.get('gcloud/bucket'),
        'processes': 4,
        'threads': 4,
    },
    'needs': [
        'bundle:gcloud',
    ],
}
    
