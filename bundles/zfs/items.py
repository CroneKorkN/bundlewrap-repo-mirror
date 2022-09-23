from json import dumps
from bundlewrap.metadata import MetadataJSONEncoder

files = {
    '/etc/cron.d/zfsutils-linux': {'delete': True, 'needs': {'pkg_apt:zfs-auto-snapshot'}},
    '/etc/cron.d/zfs-auto-snapshot': {'delete': True, 'needs': {'pkg_apt:zfs-auto-snapshot'}},
    '/etc/cron.hourly/zfs-auto-snapshot': {'delete': True, 'needs': {'pkg_apt:zfs-auto-snapshot'}},
    '/etc/cron.daily/zfs-auto-snapshot': {'delete': True, 'needs': {'pkg_apt:zfs-auto-snapshot'}},
    '/etc/cron.weekly/zfs-auto-snapshot': {'delete': True, 'needs': {'pkg_apt:zfs-auto-snapshot'}},
    '/etc/cron.monthly/zfs-auto-snapshot': {'delete': True, 'needs': {'pkg_apt:zfs-auto-snapshot'}},
    '/etc/modprobe.d/zfs.conf': {
        'content': '\n'.join(
            f'options zfs {k}={v}'
                for k, v in node.metadata.get('zfs/kernel_params').items()
        ) + '\n',
    },
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

    encrypted = zfs_datasets[name].pop('encrypted', None)
    if encrypted:
        zfs_datasets[name]['encryption'] = 'aes-256-gcm'
        zfs_datasets[name]['keylocation'] = 'prompt'
        zfs_datasets[name]['keyformat'] = 'hex'
        zfs_datasets[name]['password'] = node.metadata.get('zfs/password')


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
        "autotrim": False,
    }
