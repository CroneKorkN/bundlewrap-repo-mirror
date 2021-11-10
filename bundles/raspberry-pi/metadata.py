h = repo.libs.hashable.hashable

defaults = {
    'grafana_rows': {
        'health',
    },
    'systemd-journald': {
        'Storage': 'volatile',
    },
}


@metadata_reactor.provides(
    'telegraf/config',
)
def telegraf(metadata):
    return {
        'telegraf': {
            'config': {
                'agent': {
                    'flush_interval': '30s',
                    'interval': '30s',
                },
                'inputs': {
                    'exec': {
                        h({
                            'commands': ["/bin/bash -c 'expr $(cat /sys/class/thermal/thermal_zone0/temp) / 1000'"],
                            'name_override': "cpu_temperature",
                            'data_format': "value",
                            'data_type': "integer",
                        }),
                        # h({
                        #     'commands': [
                        #         f'sudo /usr/local/share/icinga/plugins/smartctl',
                        #     ],
                        #     'data_format': 'influx',
                        #     'interval': '20s',
                        # }),
                    },
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
            'datasets': {
                name: {
                    'logbias': 'throughput',
                }
                    for name in metadata.get('zfs/datasets')
            },
            'kernel_params': {
                'zfs_txg_timeout': 300,
            },
        },
    }
