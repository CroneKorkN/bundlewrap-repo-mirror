{
    'metadata': {
        'telegraf': {
            'config': {
                'inputs': {
                    'exec': [{
                        'commands': ["/bin/bash -c 'expr $(cat /sys/class/thermal/thermal_zone0/temp) / 1000'"],
                        'name_override': "cpu_temperature",
                        'data_format': "value",
                        'data_type': "integer",
                    }],
                },
            },
        },
        'grafana_rows': {
            'health',
        },
        'zfs': {
            'kernel_params': {
                'zfs_txg_timeout': 300,
            },
        },
    },
}
