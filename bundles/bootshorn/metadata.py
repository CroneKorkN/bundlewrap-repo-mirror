defaults = {
    'systemd': {
        'units': {
            'bootshorn-record.service': {
                'Unit': {
                    'Description': 'Bootshorn Recorder',
                    'After': 'network.target',
                },
                'Service': {
                    'User': 'ckn',
                    'Group': 'ckn',
                    'Type': 'simple',
                    'WorkingDirectory': '/opt/bootshorn',
                    'ExecStart': '/opt/bootshorn/record',
                    'Restart': 'always',
                    'RestartSec': 5,
                    'Environment': {
                        "XDG_RUNTIME_DIR": "/run/user/1000",
                        "PULSE_SERVER": "unix:/run/user/1000/pulse/native",
                    },
                },
            },
        },
    },
    'systemd-timers': {
        'bootshorn-temperature': {
            'command': '/opt/bootshorn/temperature',
            'when': '*:0/10',
            'working_dir': '/opt/bootshorn',
            'user': 'ckn',
            'group': 'ckn',
        },
        # 'bootshorn-process': {
        #     'command': '/opt/bootshorn/process',
        #     'when': 'hourly',
        #     'working_dir': '/opt/bootshorn',
        #     'user': 'ckn',
        #     'group': 'ckn',
        #     'after': {
        #         'bootshorn-process.service',
        #     },
        # },
    },
}
