from json import dumps
from bundlewrap.metadata import MetadataJSONEncoder

files = {
    '/etc/cron.d/zfsutils-linux': {'delete': True},
    '/etc/cron.d/zfs-auto-snapshot': {'delete': True},
    '/etc/cron.hourly/zfs-auto-snapshot': {'delete': True},
    '/etc/cron.daily/zfs-auto-snapshot': {'delete': True},
    '/etc/cron.weekly/zfs-auto-snapshot': {'delete': True},
    '/etc/cron.monthly/zfs-auto-snapshot': {'delete': True},
}

actions = {
    'modprobe_zfs': {
        'command': 'modprobe zfs',
        'unless': 'lsmod | grep ^zfs',
        'needs': {
            'pkg_apt:zfs-dkms',
        },
        'needed_by': {
            'pkg_apt:zfs-zed',
            'pkg_apt:zfsutils-linux',
            'zfs_dataset:',
            'zfs_pool:',
        },
        'comment': 'If this fails, do a dist-upgrade, reinstall zfs-dkms, reboot',
    },
}

svc_systemd = {
    'zfs-zed': {
        'needs': {
            'pkg_apt:zfs-zed'
        },
    },
}

for name, config in node.metadata.get('zfs/datasets', {}).items():
    zfs_datasets[name] = config
    zfs_datasets[name].pop('backup', None)

for name, config in node.metadata.get('zfs/pools', {}).items():
    zfs_pools[name] = {
        "when_creating": {
            "config": [
                {
                    "type": config.get('type', None),
                    "devices": config['devices'],
                },
            ],
        },
        "autotrim": True,
    }
