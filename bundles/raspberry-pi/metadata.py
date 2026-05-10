h = repo.libs.hashable.hashable

defaults = {
    'systemd-journald': {
        'Storage': 'volatile',
    },
}

if node.has_bundle('zfs'):
    defaults['zfs'] = {
        'kernel_params': {
            'zfs_txg_timeout': 300,
        },
    }


@metadata_reactor.provides(
    'telegraf/agent',
)
def telegraf(metadata):
    metadata.get('telegraf/agent')  # only override if telegraf bundle is present
    return {
        'telegraf': {
            'agent': {
                'flush_interval': '30s',
                'interval': '1m',
            },
        },
    }
