defaults = {
    'archive': {},
}


@metadata_reactor.provides(
    'gocryptfs/paths',
)
def gocryptfs(metadata):
    paths = {}
    
    for path in metadata.get('archive/paths'):
        paths[path] = {
            'mountpoint': f'/mnt/gocryptfs{path}',
            'reverse': True,
        } 

    return {
        'gocryptfs': {
            'paths': paths,
        },
    }
