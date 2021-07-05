for group, config in node.metadata.get('groups', {}).items():
    groups[group] = config

for name, config in node.metadata.get('users').items():
    directories[config['home']] = {
        'owner': name,
        'mode': '700',
    }

    files[f"{config['home']}/.ssh/id_{config['keytype']}"] = {
        'content': config['privkey'] + '\n',
        'owner': name,
        'mode': '0600',
    }
    files[f"{config['home']}/.ssh/id_{config['keytype']}.pub"] = {
        'content': config['pubkey'] + '\n',
        'owner': name,
        'mode': '0600',
    }
    files[config['home'] + '/.ssh/authorized_keys'] = {
        'content': '\n'.join(sorted(config['authorized_keys'])) + '\n',
        'owner': name,
        'mode': '0600',
    }

    users[name] = config
    for option in ['authorized_keys', 'authorized_users', 'privkey', 'pubkey', 'keytype']:
        users[name].pop(option, None)
