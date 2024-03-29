defaults = {
    'apt': {
        'packages': {
            'nodejs': {},
            # http://www.alvinsim.com/which-yarn/
            'cmdtest': {
                'installed': False,
            },
        },
    },
    'npm': {
        'yarn': {},
    },
}


@metadata_reactor.provides(
    'apt/sources',
)
def sources(metadata):
    version = metadata.get('nodejs/version')

    return {
        'apt': {
            'sources': {
                'nodesource': {
                    'types': {
                        'deb',
                        'deb-src',
                    },
                    'url': 'https://deb.nodesource.com/node_{version}.x',
                    'suites': {
                        '{codename}',
                    },
                    'components': {
                        'main',
                    },
                },
            },
        },
    }
