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
