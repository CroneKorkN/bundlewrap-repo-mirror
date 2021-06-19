from glob import glob
from os.path import join, basename

defaults = {
    'apt': {
        'packages': {},
        'sources': {},
        'keys': [],
    },
}


@metadata_reactor.provides(
    'apt/keys',
)
def keys(metadata):
    keys = []
    
    for name in node.metadata.get('apt/sources'):
        matches = glob(join(repo.path, 'data', 'apt', 'keys', f'{name}.*'))

        if matches:
            assert len(matches) == 1
            keys.append(basename(matches[0]))

    return {
        'apt': {
            'keys': keys,
        },
    }

 
