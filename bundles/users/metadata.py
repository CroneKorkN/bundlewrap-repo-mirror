@metadata_reactor.provides(
    'users',
)
def user(metadata):
    users = {}

    for name, config in metadata.get('users').items():
        users[name] = {
            'authorized_keys': [],
            'privkey': '111',
            'privkey': 'pubkey',
        }
    
    return {
        'users': users,
    }
