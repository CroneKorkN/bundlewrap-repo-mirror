{
    'supergroups': [
        'linux',
    ],
    'bundles': [
        'apt',
    ],
    'metadata': {
        'apt': {
            'sources': {
                'deb http://deb.debian.org/debian {release} main non-free contrib',
                'deb http://deb.debian.org/debian {release}-updates main contrib non-free',
                'deb http://deb.debian.org/debian {release}-backports main contrib non-free',
            },
            'packages': {
                'mtr-tiny': {},
            },
        },
    },
    'os': 'debian',
    'pip_command': 'pip3',
}
