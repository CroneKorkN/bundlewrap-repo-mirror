files = {
    '/etc/icingaweb2/setup.token': {
        'content': node.metadata.get('icingaweb2/setup_token'),
        'owner': 'nagios',
    },
}
