h = repo.libs.hashable.hashable

defaults = {
    'systemd-journald': {
        'Storage': 'volatile',
    },
}


@metadata_reactor.provides(
    'telegraf/config/agent',
)
def telegraf(metadata):
    return {
        'telegraf': {
            'config': {
                'agent': {
                    'flush_interval': '30s',
                    'interval': '30s',
                },
            },
        },
    }


@metadata_reactor.provides(
    'zfs/kernel_params',
    'zfs/datasets',
)
def zfs(metadata):
    if not node.has_bundle('zfs'):
        return {}

    return {
        'zfs': {
            'kernel_params': {
                'zfs_txg_timeout': 300,
            },
        },
    }
