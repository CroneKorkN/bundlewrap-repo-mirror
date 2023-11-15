debian_version = min([node.os_version, (11,)])[0] # FIXME

defaults = {
    'apt': {
        'packages': {
            'crystal': {},
        },
        'sources': {
            'crystal': {
                # https://software.opensuse.org/download.html?project=devel%3Alanguages%3Acrystal&package=crystal
                'urls': {
                    'http://download.opensuse.org/repositories/devel:/languages:/crystal/Debian_Testing/',
                },
                'suites': {
                    '/',
                },
            },
        },
    },
}
