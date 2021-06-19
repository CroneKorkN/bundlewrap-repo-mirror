defaults = {
    'gocryptfs': {},
}


@metadata_reactor.provides(
    'gocryptfs',
)
def gocryptfs(metadata):
    gocryptfs = {}
    
    for path, options in metadata.get('gocryptfs'):
        gocryptfs[path] = {
        } 

    return {
        'gocryptfs': gocryptfs,
    }
