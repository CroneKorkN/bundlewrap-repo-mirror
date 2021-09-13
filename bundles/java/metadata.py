assert node.os == 'debian'

if node.os_version == (10,):
    version = 11
elif node.os_version == (11,):
    version = 17
else:
    raise Exception('java bundle doesnt support this os and version')

defaults = {
    'apt': {
        'packages': {
            f'openjdk-{version}-jre': {},
        }
    }
}
