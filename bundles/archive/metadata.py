defaults = {
    'archive': {},
}


@metadata_reactor.provides(
    'gocryptfs',
)
def gocryptfs(metadata):
    gocryptfs = {}
    
    for path in metadata.get('archive'):
        gocryptfs[path] = {
            'mountpoint': f'/mnt/gocryptfs{path}',
            'reverse': True,
        } 

    return {
        'gocryptfs': gocryptfs,
    }
