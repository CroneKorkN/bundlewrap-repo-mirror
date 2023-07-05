debian_version = min([node.os_version, (11,)])[0] # FIXME

defaults = {
    'apt': {
        'packages': {
            'crystal': {},
        },
        'sources': {
            f'deb https://download.opensuse.org/repositories/devel:/languages:/crystal/Debian_{debian_version}/ /',
        },
    },
}
