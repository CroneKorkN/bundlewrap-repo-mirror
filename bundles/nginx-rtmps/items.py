files = {
    '/etc/nginx/conf.d/rtmps.conf': {
        'content_type': 'mako',
        'context': {
            'server_name': node.metadata.get('nginx-rtmps/hostname'),
            'stream_key': node.metadata.get('nginx-rtmps/stream_key'),
        }
    },
}
