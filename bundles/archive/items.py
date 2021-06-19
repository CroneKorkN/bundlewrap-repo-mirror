assert node.has_bundle('gcloud')

files['/opt/archive'] = {
    'content_type': 'mako',
    'mode': '700',
    'context': {
        'dirs': node.metadata.get('archive'),
        'bucket': node.metadata.get('gcloud/bucket'),
        'processes': 4,
        'threads': 16,
    },
    'needs': [
        'bundle:gcloud',
    ],
}
    
