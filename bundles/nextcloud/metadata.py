defaults = {
    'archive': { 
        '/var/lib/nextcloud/': {
            'exclude': [
                '^appdata_',
                '^updater-',
                '^nextcloud\.log',
                '^updater\.log',
                '^[^/]+/cache',
                '^[^/]+/files_versions',
                '^[^/]+/files_trashbin',
            ],
        }
    },
}


@metadata_reactor.provides(
    'archive',
)
def exclude_hidden_files_from_archive(metadata):
    return {
        'archive': {
            dir: {
                'exclude': [
                    '^\..*',
                    '/\..*',
                ],
            } for dir, conf in metadata.get('archive').items()
        }
    }
