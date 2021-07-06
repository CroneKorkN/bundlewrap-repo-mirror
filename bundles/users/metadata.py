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
def authorized_users(metadata):
    users = {}

    for name, config in metadata.get('users').items():
        users[name] = {
            'authorized_keys': [],
        }
        for authorized_user in config.get('authorized_users', []):
            authorized_user_name, authorized_user_node = authorized_user.split('@')
            users[name]['authorized_keys'].append(
                repo.get_node(authorized_user_node).metadata.get(f'users/{authorized_user_name}/pubkey')
            )
    return {
        'users': users,
    }


# FIXME: bw bug?
# @metadata_reactor.provides(
#     'users',
# )
@metadata_reactor
def user(metadata):
    users = {}

    for name, config in metadata.get('users').items():
        users[name] = {
            'authorized_keys': [],
        }

        if not 'full_name' in config:
            users[name]['full_name'] = name

        if not 'home' in config:
            users[name]['home'] = f'/home/{name}'

        if not 'shell' in config:
            users[name]['shell'] = '/bin/bash'
            
        if not 'privkey' in users[name] and not 'pubkey' in users[name]:
            privkey, pubkey = repo.libs.ssh.generate_ed25519_key_pair(
                b64decode(str(repo.vault.random_bytes_as_base64_for(f"{name}@{metadata.get('id')}", length=32)))
            )
            users[name]['keytype'] = 'ed25519'
            users[name]['privkey'] = privkey
            users[name]['pubkey'] = pubkey + f' {name}@{node.name}'
    
    return {
        'users': users,
    }
