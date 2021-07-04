{
    'stacked': True,
    'targets': [
        {
            '_measurement': 'cpu',
            'cpu': 'cpu-total',
            '_field': [
                'usage_iowait',
                'usage_system',
                'usage_user',
            ],
        },
    ],
}
