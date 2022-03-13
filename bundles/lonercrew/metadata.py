if not node.has_bundle('build-ci'):
    raise Exception('lownercrew needs bundle build-ci')


defaults = {
    'build-ci': {
        'lonercrew': {
            'path': '/opt/lonercrew',
            'group': 'www-data',
            'branch': 'master',
        },
    },
}


@metadata_reactor.provides(
    'nginx/vhosts',
)
def nginx(metadata):
    return {
        'nginx': {
            'vhosts': {
                'lonercrew.io': {
                    'content': 'lonercrew/vhost.conf',
                },
            },
        },
    }
