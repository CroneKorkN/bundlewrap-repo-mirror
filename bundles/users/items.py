from os.path import join, exists

for group, attrs in node.metadata.get('groups', {}).items():
    groups[group] = attrs

for username, attrs in node.metadata['users'].items():
    home = attrs.get('home', '/home/{}'.format(username))

    user = users.setdefault(username, {})

    user['home'] = home
    user['shell'] = attrs.get('shell', '/bin/bash')

    if 'password' in attrs:
        user['password'] = attrs['password']
    else:
        user['password_hash'] = 'x' if node.use_shadow_passwords else '*'

    if 'groups' in attrs:
        user['groups'] = attrs['groups']

    directories[home] = {
        'owner': username,
        'mode': attrs.get('home-mode', '0700'),
    }

    if 'ssh_pubkey' in attrs:
        files[home + '/.ssh/authorized_keys'] = {
            'content': '\n'.join(sorted(attrs['ssh_pubkey'])) + '\n',
            'owner': username,
            'mode': '0600',
        }

    elif not attrs.get('do_not_remove_authorized_keys_from_home', False):
        files[home + '/.ssh/authorized_keys'] = {'delete': True}
