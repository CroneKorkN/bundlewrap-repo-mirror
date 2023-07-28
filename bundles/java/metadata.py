assert node.os == 'debian'


defaults = {
    'java': {
        'version': {
            10: 11,
            11: 17,
            12: 17,
        }[node.os_version[0]],
    },
}


@metadata_reactor.provides(
    'apt/packages',
)
def apt(metadata):
    return {
        'apt': {
            'packages': {
                f'openjdk-{metadata.get("java/version")}-jre-headless': {},
            }
        }
    }
