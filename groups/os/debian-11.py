{
    'supergroups': [
        'debian',
    ],
    'metadata': {
        'apt': {
            'sources': {
                'deb https://deb.debian.org/debian {codename} main contrib non-free',
                'deb https://deb.debian.org/debian {codename}-updates main contrib non-free',
                'deb https://deb.debian.org/debian {codename}-backports main contrib non-free',
                'deb https://security.debian.org/ {codename}-security main contrib non-free',
            },
        },
        'php': {
            'version': '7.4',
        },
        'postgresql': {
            'version': '13',
        },
        'os_codename': 'bullseye',
    },
    'os_version': (11,),
}
