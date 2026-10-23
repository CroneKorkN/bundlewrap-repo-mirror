defaults = {
    'apt': {
        'packages': {
            'crystal': {},
            # static linking (crystal build --static)
            'build-essential': {},
            'libgc-dev': {},
            'libpcre2-dev': {},
            'libevent-dev': {},
        },
        'sources': {
            'crystal': {
                # https://software.opensuse.org/download.html?project=devel%3Alanguages%3Acrystal&package=crystal
                # curl -fsSL https://download.opensuse.org/repositories/devel:/languages:/crystal/Debian_13/Release.key
                'urls': {
                    f'http://download.opensuse.org/repositories/devel:/languages:/crystal/Debian_{node.os_version[0]}/',
                },
                'suites': {
                    '/',
                },
            },
        },
    },
}
