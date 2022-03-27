from base64 import b64decode


@metadata_reactor.provides(
    'ssh/allow_users',
)
def users(metadata):
    return {
        'ssh': {
            'allow_users': set(
                name
                    for name, conf in metadata.get('users').items()
                    if conf.get('authorized_keys', []) or conf.get('authorized_users', [])
            ),
        },
    }


@metadata_reactor.provides(
    'ssh/host_key',
)
def host_key(metadata):
    private, public = repo.libs.ssh.generate_ed25519_key_pair(
        b64decode(str(repo.vault.random_bytes_as_base64_for(f"HostKey {metadata.get('id')}", length=32)))
    )

    return {
        'ssh': {
            'host_key': {
                'private': private + '\n',
                'public': public + f' root@{node.name}',
            }
        },
    }
