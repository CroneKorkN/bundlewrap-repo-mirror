for group, config in node.metadata.get('groups', {}).items():
    groups[group] = config

for name, config in node.metadata.get('users').items():
    directories[config['home']] = {
        'owner': config.get('home_owner', name),
        'group': config.get('home_group', name),
        'mode': config.get('home_mode', '700'),
    }

    directories[f"{config['home']}/.ssh"] = {
        'owner': config.get('home_owner', name),
        'group': config.get('home_group', name),
        'mode': '0700',
    }

    files[f"{config['home']}/.ssh/id_{config['keytype']}"] = {
        'content': config['privkey'] + '\n',
        'owner': name,
        'mode': '0600',
        'tags': [
            'ssh_users',
        ],
    }
    files[f"{config['home']}/.ssh/id_{config['keytype']}.pub"] = {
        'content': config['pubkey'] + '\n',
        'owner': name,
        'mode': '0600',
        'tags': [
            'ssh_users',
        ],
    }
    files[config['home'] + '/.ssh/authorized_keys'] = {
        'content': '\n'.join(sorted(config['authorized_keys'])) + '\n',
        'owner': name,
        'mode': '0600',
        'tags': [
            'ssh_users',
        ],
    }

    users[name] = config
    for option in ['authorized_keys', 'authorized_users', 'privkey', 'pubkey', 'keytype', 'home_owner', 'home_group', 'home_mode']:
        users[name].pop(option, None)
