directories = {
    '/etc/sudoers.d': {
        'mode': '0750',
        'purge': True,
    },
}

for user, commands in node.metadata.get('sudoers').items():
    files[f'/etc/sudoers.d/{user}'] = {
        'content_type': 'mako',
        'source': 'sudoer',
        'context': {
            'user': user,
            'commands': commands,
        },
        'mode': '500',
    }
