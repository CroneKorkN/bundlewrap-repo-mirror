icinga_node = repo.get_node(node.metadata.get('monitoring/icinga2_node'))

files = {
    '/usr/local/bin/downtime': {
        'content_type': 'mako',
        'mode': '0750',
        'context': {
            'node_name': node.name,
            'icinga_hostname': icinga_node.metadata.get('icinga2/hostname'),
            'icinga_password': icinga_node.metadata.get('icinga2/api_users/root/password'),
        },
    },
}
