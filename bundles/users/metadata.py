from base64 import b64decode


defaults = {
    'users': {
        'root': {
            'home': '/root',
        },
    },
}


@metadata_reactor.provides(
    'users',
)
def users(metadata):
    users = {}

    for name in metadata.get('users'):
        privkey, pubkey = repo.libs.ssh.generate_ad25519_key_pair(
            b64decode(str(repo.vault.random_bytes_as_base64_for(metadata.get('id'), length=32)))
        )
        users[name] = {
            'home': f'/home/{name}',
            'privkey': privkey,
            'pubkey': pubkey,
        }
    
    return {
        'users': users,
    }
