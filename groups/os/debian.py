{
    'supergroups': [
        'linux',
    ],
    'bundles': [
        'apt',
        'nftables',
    ],
    'metadata': {
        'apt': {
            'sources': {
                'deb https://deb.debian.org/debian {release} main contrib non-free',
                'deb https://deb.debian.org/debian {release}-updates main contrib non-free',
                'deb https://deb.debian.org/debian {release}-backports main contrib non-free',
                'deb https://security.debian.org/ {release}-security main contrib non-free',
            },
            'packages': {
                'mtr-tiny': {},
            },
        },
    },
    'os': 'debian',
    'pip_command': 'pip3',
}
