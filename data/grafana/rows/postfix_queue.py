{
    'length': {
        'stacked': True,
        'queries': {
            'length': {
                'filters': {
                    '_measurement': 'postfix_queue',
                    '_field': [
                        'length',
                    ],
                },
                'function': 'max',
            },
        },
        'display_name': '${__field.labels.queue}'
    },
    'size': {
        'stacked': True,
        'queries': {
            'size': {
                'filters': {
                    '_measurement': 'postfix_queue',
                    '_field': [
                        'size',
                    ],
                },
                'function': 'max',
            },
        },
        'display_name': '${__field.labels.queue}'
    },
    'age': {
        'stacked': True,
        'queries': {
            'age': {
                'filters': {
                    '_measurement': 'postfix_queue',
                    '_field': [
                        'age',
                    ],
                },
                'function': 'max',
            },
        },
        'display_name': '${__field.labels.queue}'
    },
}
