@metadata_reactor.provides(
    'ssh/allow_users',
)
def users(metadata):
    return {
        'ssh': {
            'allow_users': set(
                name
                    for name, conf in metadata.get('users').items()
                    if conf.get('authorized_keys', []) or conf.get('authorized_users', [])
            ),
        },
    }
