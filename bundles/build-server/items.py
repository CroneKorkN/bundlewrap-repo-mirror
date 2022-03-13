import json
from bundlewrap.metadata import MetadataJSONEncoder

directories = {
    '/opt/build-server/strategies': {
        'owner': 'build-server',
    },
}

files = {
    '/etc/build-server.json': {
        'owner': 'build-server',
        'content': json.dumps(node.metadata.get('build-server'), indent=4, sort_keys=True, cls=MetadataJSONEncoder)
    },
    '/opt/build-server/strategies/crystal': {
        'content_type': 'mako',
        'owner': 'build-server',
        'mode': '0777', # FIXME
        'context': {
            'config_path': '/etc/build-server.json',
            'download_server': node.metadata.get('build-server/download_server_ip'),
        },
    },
    '/opt/build-server/strategies/ci': {
        'content_type': 'mako',
        'owner': 'build-server',
        'mode': '0777', # FIXME
        'context': {
            'config_path': '/etc/build-server.json',
        },
    },
}
