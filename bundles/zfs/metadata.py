#import re

defaults = {
    'apt': {
        'packages': {
            'parted':{
                'needed_by': {
                    'pkg_apt:zfs-zed',
                    'pkg_apt:zfsutils-linux',
                },
            },
            'zfs-dkms': {
                'backports': node.os_version < (11,),
                'needed_by': {
                    'pkg_apt:zfs-zed',
                    'pkg_apt:zfsutils-linux',
                },
            },
            'zfs-zed': {
                'backports': node.os_version < (11,),
                'needed_by': {
                    'zfs_dataset:',
                    'zfs_pool:',
                },
            },
            'zfsutils-linux': {
                'backports': node.os_version < (11,),
                'needed_by': {
                    'pkg_apt:zfs-zed',
                    'zfs_dataset:',
                    'zfs_pool:',
                },
            },
            'zfs-auto-snapshot': {},
        },
    },
    'systemd-timers': {
        'zfs-trim': {
            'command': '/usr/lib/zfs-linux/trim',
            'when': '*-*-01 00:00:00',
            'persistent': True,
        },
        'zfs-scrub': {
            'command': '/usr/lib/zfs-linux/scrub',
            'when': '*-*-15 00:00:00',
            'persistent': True,
        },
        'zfs-auto-snapshot-hourly': {
            'command': '/usr/sbin/zfs-auto-snapshot --quiet --syslog --label=hourly --keep=24 //',
            'when': 'hourly',
        },
        'zfs-auto-snapshot-daily': {
            'command': '/usr/sbin/zfs-auto-snapshot --quiet --syslog --label=daily --keep=7 //',
            'when': 'daily',
        },
        'zfs-auto-snapshot-weekly': {
            'command': '/usr/sbin/zfs-auto-snapshot --quiet --syslog --label=weekly --keep=4 //',
            'when': 'weekly',
            'persistent': True,
        },
        'zfs-auto-snapshot-monthly': {
            'command': '/usr/sbin/zfs-auto-snapshot --quiet --syslog --label=monthly --keep=24 //',
            'when': 'monthly',
            'persistent': True,
        },
    },
    'telegraf': {
        'config': {
            'inputs': {
                'zfs': [{}],
            },
        },
    },
    'grafana_rows': {
        'zfs_arc',
    },
    'zfs': {
        'datasets': {},
        'pools': {},
        'kernel_params': {},
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
                    'relatime': 'on',
                } for name, config in metadata.get('zfs/datasets').items()
            },
        },
    }


@metadata_reactor.provides(
    'backup/paths'
)
def backup(metadata):
    return {
        'backup': {
            'paths': {
                options['mountpoint']
                    for options in metadata.get('zfs/datasets').values()
                    if options.get('backup', True)
            },
        },
    }


@metadata_reactor.provides(
    'apt/packages'
)
def headers(metadata):
    if node.in_group('raspberry-pi'):
        arch = 'arm64'
    else:
        arch = 'amd64'
    
    return {
        'apt': {
            'packages': {
                f'linux-headers-{arch}': {
                    'needed_by': {
                        'pkg_apt:zfs-dkms',
                    },
                },
            },
        },
    }
