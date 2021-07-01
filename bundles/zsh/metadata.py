defaults = {
    'apt': {
        'packages': {
            'zsh': {},
        }
    }
}

@metadata_reactor.provides(
    'users'
)
def users(metadata):
    return {
        'users': {
            'user'
        }
    }
