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
    '/usr/lib/nagios/plugins/check_zpool_space': {
        'mode': '0755',
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
