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
            'deb https://packages.cloud.google.com/apt cloud-sdk main',
        },
    },
}
