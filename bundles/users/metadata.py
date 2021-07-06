@metadata_reactor.provides(
    'users',
)
def user(metadata):
    users = {}

    for name, config in metadata.get('users').items():
        users[name] = {
            'pubkey': '222',
        }
    
    return {
        'users': users,
    }
