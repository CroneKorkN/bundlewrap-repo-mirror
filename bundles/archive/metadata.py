defaults = {
    'apt': {
        'packages': {
            'jq': {},
        },
    },
    'archive': {
        'paths': {},
    },
}


@metadata_reactor.provides(
    'archive/paths',
)
def paths(metadata):
    return {
        'archive': {
            'paths': {
                path: {
                    'encrypted_path': f'/mnt/archive.enc{path}',
                    'exclude': [
                        '^\..*',
                        '/\..*',
                    ],
                } for path in metadata.get('archive/paths')
            },
        }
    }


@metadata_reactor.provides(
    'gocryptfs/paths',
)
def gocryptfs(metadata):
    return {
        'gocryptfs': {
            'paths': {
                path: {
                    'mountpoint': options['encrypted_path'],
                    'reverse': True,
                } for path, options in metadata.get('archive/paths').items()
            },
        }
    }
