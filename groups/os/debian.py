{
    'supergroups': [
        'linux',
    ],
    'bundles': [
        'apt',
        'nftables',
        'pip',
    ],
    'metadata': {
        'apt': {
            'sources': {
                'deb https://deb.debian.org/debian {codename} main contrib non-free',
                'deb https://deb.debian.org/debian {codename}-updates main contrib non-free',
                'deb https://deb.debian.org/debian {codename}-backports main contrib non-free',
                'deb https://security.debian.org/ {codename}-security main contrib non-free',
            },
            'packages': {
                'mtr-tiny': {},
            },
        },
    },
    'os': 'debian',
    'pip_command': 'pip3',
}
