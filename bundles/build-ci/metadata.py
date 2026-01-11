from shlex import quote


defaults = {
    'build-ci': {},
}

@metadata_reactor.provides(
    'users/build-ci/authorized_users',
    'sudoers/build-ci',
)
def ssh_keys(metadata):
    return {
        'users': {
            'build-ci': {
                'authorized_users': {
                    f'build-server@{other_node.name}': {}
                        for other_node in repo.nodes
                        if other_node.has_bundle('build-server')
                },
            },
        },
        'sudoers': {
            'build-ci': {
                f"/usr/bin/chown -R build-ci\\:{quote(ci['group'])} {quote(ci['path'])}"
                    for ci in metadata.get('build-ci').values()
            }
        },
    }
