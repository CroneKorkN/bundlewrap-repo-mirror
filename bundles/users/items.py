for group, config in node.metadata.get('groups', {}).items():
    groups[group] = config

for name, config in node.metadata.get('users').items():
    users[name] = {
        k:v for k,v in config.items() if k in [
            "full_name", "gid", "groups", "home", "password_hash", "shell", "uid", 
        ]
    }

    directories[config['home']] = {
        'owner': name,
        'mode': '700',
    }

    files[f"{config['home']}/.ssh/id_{config['keytype']}"] = {
        'content': config['privkey'],
        'owner': name,
        'mode': '0600',
    }
    files[f"{config['home']}/.ssh/id_{config['keytype']}.pub"] = {
        'content': config['pubkey'],
        'owner': name,
        'mode': '0600',
    }
    files[config['home'] + '/.ssh/authorized_keys'] = {
        'content': '\n'.join(sorted(config['authorized_keys'])),
        'owner': name,
        'mode': '0600',
    }
