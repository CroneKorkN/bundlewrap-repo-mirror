from os.path import join

for name, user_config in node.metadata.get('users').items():
    if user_config.get('shell', None) != '/usr/bin/zsh':
        continue

    directories = {
        join(user_config['home'], '.zsh'): {
            'owner': name,
            'group': name,
        },
        join(user_config['home'], '.zsh/oh-my-zsh'): {
            'owner': name,
            'group': name,
        },
        join(user_config['home'], '.zsh/oh-my-zsh/custom/plugins/zsh-autosuggestions'): {
            'owner': name,
            'group': name,
            'needs': [
                f"git_deploy:{join(user_config['home'], '.zsh/oh-my-zsh')}",
            ]
        },
    }

    git_deploy = {
        join(user_config['home'], '.zsh/oh-my-zsh'): {
            'repo': 'https://github.com/ohmyzsh/ohmyzsh.git',
            'rev': 'master',
            'triggers': [
                f'action:chown_zsh_{name}',
            ],
        },
        join(user_config['home'], '.zsh/oh-my-zsh/custom/plugins/zsh-autosuggestions'): {
            'repo': 'https://github.com/zsh-users/zsh-autosuggestions.git',
            'rev': 'master',
            'triggers': [
                f'action:chown_zsh_{name}',
            ],
        },
    }

    files = {
        join(user_config['home'], '.zshrc'): {
            'owner': name,
            'group': name,
            'source': 'zshrc',
        },
        join(user_config['home'], '.zsh/oh-my-zsh/themes/bw.zsh-theme'): {
            'owner': name,
            'group': name,
            'needs': [
                f"git_deploy:{join(user_config['home'], '.zsh/oh-my-zsh')}",
            ]
        },
    }

    actions = {
        f'chown_zsh_{name}': {
            'command': f"chown -R {name}:{name} {user_config['home']}",
            'triggered': True,
        },
    }
