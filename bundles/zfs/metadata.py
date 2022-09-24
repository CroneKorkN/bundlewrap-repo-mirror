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
    'monitoring': {
        'services': {
            'zpool space': {
                'vars.command': f'/usr/lib/nagios/plugins/check_zpool_space',
            },
        },
    },
    'systemd-timers': {
        'zfs-trim': {
            'command': '/usr/lib/zfs-linux/trim',
            'when': '*-*-16 02:00',
            'persistent': True,
        },
        'zfs-scrub': {
            'command': '/usr/lib/zfs-linux/scrub',
            'when': '*-2,4,6,8,10,12-1 02:00',
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
        'storage_classes': {
            'hdd': 'tank',
        },
        'auto_snapshots': {
            'hourly': 24,
            'daily': 7,
            'weekly': 4,
            'monthly': 24,
        },
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
                    and not options.get('mountpoint', None) in [None, 'none']
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


@metadata_reactor.provides(
    'zfs/kernel_params/zfs_arc_max',
)
def arc_size(metadata):
    arc_percent = metadata.get('zfs/zfs_arc_max_percent', None)

    if arc_percent:
        return {
            'zfs': {
                'kernel_params': {
                    'zfs_arc_max': str(int(
                        metadata.get('vm/ram') * 1024 * 1024 * (arc_percent/100)
                    )),
                },
            },
        }
    else:
        return {}


@metadata_reactor.provides(
    'systemd-timers/zfs-auto-snapshot-hourly',
    'systemd-timers/zfs-auto-snapshot-daily',
    'systemd-timers/zfs-auto-snapshot-weekly',
    'systemd-timers/zfs-auto-snapshot-monthly',
)
def auto_snapshots(metadata):
    hourly = metadata.get('zfs/auto_snapshots/hourly')
    daily = metadata.get('zfs/auto_snapshots/daily')
    weekly = metadata.get('zfs/auto_snapshots/weekly')
    monthly = metadata.get('zfs/auto_snapshots/monthly')

    # cant be 0
    assert hourly > 0 and daily > 0 and weekly > 0 and monthly > 0

    return {
        'systemd-timers': {
            'zfs-auto-snapshot-hourly': {
                'command': f'/usr/sbin/zfs-auto-snapshot --quiet --syslog --label=hourly --keep={hourly} //',
                'when': 'hourly',
            },
            'zfs-auto-snapshot-daily': {
                'command': f'/usr/sbin/zfs-auto-snapshot --quiet --syslog --label=daily --keep={daily} //',
                'when': 'daily',
            },
            'zfs-auto-snapshot-weekly': {
                'command': f'/usr/sbin/zfs-auto-snapshot --quiet --syslog --label=weekly --keep={weekly} //',
                'when': 'weekly',
                'persistent': True,
            },
            'zfs-auto-snapshot-monthly': {
                'command': f'/usr/sbin/zfs-auto-snapshot --quiet --syslog --label=monthly --keep={monthly} //',
                'when': 'monthly',
                'persistent': True,
            },
        },
    }
