#import re

defaults = {
    'apt': {
        'packages': {
            'linux-headers-amd64': {
                'needed_by': {
                    'pkg_apt:zfs-dkms',
                },
            },
            'parted':{
                'needed_by': {
                    'pkg_apt:zfs-zed',
                    'pkg_apt:zfsutils-linux',
                },
            },
            'zfs-dkms': {
                'needed_by': {
                    'pkg_apt:zfs-zed',
                    'pkg_apt:zfsutils-linux',
                },
            },
            'zfs-zed': {
                'needed_by': {
                    'zfs_dataset:',
                    'zfs_pool:',
                },
            },
            'zfsutils-linux': {
                'needed_by': {
                    'pkg_apt:zfs-zed',
                    'zfs_dataset:',
                    'zfs_pool:',
                },
            },
        },
    },
    'zfs': {
        'datasets': {},
        'pools': {},
    },
}

@metadata_reactor.provides(
    'zfs/datasets'
)
def dataset_defaults(metadata):
    return {
        'zfs': {
            'datasets': {
                name: {
                    'compression': 'lz4',
                } for name, config in metadata.get('zfs/datasets').items()
            },
        },
    }
