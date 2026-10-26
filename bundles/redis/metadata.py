defaults = {
    'apt': {
        'packages': {
            'redis-server': {},
        },
    },
    'backup': {
        'paths': {
            '/var/lib/redis',
        },
    },
    # one instance per client: {name: settings that differ from CONFIG in items.py}; a key replaces the default.
    # a cache sets save to '""' and leaves nothing for the backup
    'redis': {},
}

if node.has_bundle('zfs'):
    defaults['zfs'] = {
        'datasets': {
            'tank/redis': {
                'mountpoint': '/var/lib/redis',
                # every dump rewrites the whole file, snapshots would keep each version; the backup is enough
                'com.sun:auto-snapshot': 'false',
                'needed_by': [
                    'pkg_apt:redis-server',
                    'directory:/var/lib/redis',
                ],
            },
        },
    }
