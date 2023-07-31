defaults = {
    'apt': {
        'packages': {
            'apt-transport-https': {},
            'ca-certificates': {},
            'gnupg': {},
            'google-cloud-sdk': {},
            'python3-crcmod': {},
        },
        'sources': {
            'google-cloud': {
                'url': 'https://packages.cloud.google.com/apt/',
                'suites': {
                    'cloud-sdk',
                },
                'components': {
                    'main',
                },
            },
        },
    },
}
