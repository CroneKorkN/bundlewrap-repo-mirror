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
                'debian': '\n'.join([
                    'deb http://deb.debian.org/debian {release} main non-free contrib',
                    'deb http://deb.debian.org/debian {release}-updates main contrib non-free',
                    'deb http://security.debian.org/debian-security {release}/updates main contrib non-free',
                    'deb http://deb.debian.org/debian {release}-backports main contrib non-free',
                ]),
            },
        },
    },
    'os': 'debian',
    'pip_command': 'pip3',
}
