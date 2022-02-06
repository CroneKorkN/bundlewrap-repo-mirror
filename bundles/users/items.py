for group, config in node.metadata.get('groups', {}).items():
    groups[group] = config

for name, config in node.metadata.get('users').items():
    directories[config['home']] = {
        'owner': config.get('home_owner', name),
        'group': config.get('home_group', name),
        'mode': config.get('home_mode', '700'),
    }
    
    ssh_dir = config.get('ssh_dir', f"{config['home']}/.ssh")

    directories[ssh_dir] = {
        'owner': config.get('home_owner', name),
        'group': config.get('home_group', name),
        'mode': '0700',
    }

    files[f"{ssh_dir}/id_{config['keytype']}"] = {
        'content': config['privkey'] + '\n',
        'owner': name,
        'mode': '0600',
        'tags': [
            'ssh_users',
        ],
    }
    files[f"{ssh_dir}/id_{config['keytype']}.pub"] = {
        'content': config['pubkey'] + '\n',
        'owner': name,
        'mode': '0600',
        'tags': [
            'ssh_users',
        ],
    }
    files[f"{ssh_dir}/authorized_keys"] = {
        'content': '\n'.join(sorted(config['authorized_keys'])) + '\n',
        'owner': name,
        'mode': '0600',
        'tags': [
            'ssh_users',
        ],
    }

    users[name] = config
    for option in ['authorized_keys', 'authorized_users', 'privkey', 'pubkey', 'keytype', 'home_owner', 'home_group', 'home_mode', 'ssh_dir']:
        users[name].pop(option, None)
