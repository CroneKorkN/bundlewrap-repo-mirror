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
        'content': json.dumps(node.metadata.get('build-server'), indent=4, cls=MetadataJSONEncoder)
    },
    '/opt/build-server/build-server-crystal': {
        'content_type': 'download',
        'source': 'https://dl.sublimity.de/build-server-crystal/build-server-crystal-amd64-latest',
        'owner': 'build-server',
        'mode': '500',
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
}

svc_systemd = {
    'build-server': {
        'needs': {
            'file:/etc/systemd/system/build-server.service',
        },
    },
}
