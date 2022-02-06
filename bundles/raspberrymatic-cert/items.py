files = {
    '/opt/raspberrymatic-cert': {
        'content_type': 'mako',
        'mode': '500',
        'context': {
            'domain': node.metadata.get('raspberrymatic-cert/domain'),
            'hostname': repo.get_node(node.metadata.get('raspberrymatic-cert/node')).metadata.get('hostname'),
        }
    }
}
