{
    'metadata': {
        'telegraf': {
            'config': {
                'inputs': {
                    'exec': [{
                        'commands': ["/bin/bash -c \"cat /sys/class/thermal/thermal_zone0/temp | xargs -I '{}' expr {} / 1000\""],
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
    },
}
