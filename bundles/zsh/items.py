from os.path import join

directories = {
    '/etc/zsh/oh-my-zsh': {},
    '/etc/zsh/oh-my-zsh/custom/plugins': {
        'mode': '0755',
        'needs': [
            f"git_deploy:/etc/zsh/oh-my-zsh",
        ]
    },
    '/etc/zsh/oh-my-zsh/custom/plugins/zsh-autosuggestions': {
        'needs': [
            f"git_deploy:/etc/zsh/oh-my-zsh",
        ]
    },
}

git_deploy = {
    '/etc/zsh/oh-my-zsh': {
        'repo': 'https://github.com/ohmyzsh/ohmyzsh.git',
        'rev': 'master',
    },
    '/etc/zsh/oh-my-zsh/custom/plugins/zsh-autosuggestions': {
        'repo': 'https://github.com/zsh-users/zsh-autosuggestions.git',
        'rev': 'master',
    },
}

files = {
    '/etc/zsh/zprofile': {},
    '/etc/zsh/oh-my-zsh/themes/bw.zsh-theme': {
        'needs': [
            f"git_deploy:/etc/zsh/oh-my-zsh",
        ]
    },
}

for name, user_config in node.metadata.get('users').items():
    if user_config.get('shell', None) != '/usr/bin/zsh':
        files[join(user_config['home'], '.zshrc')] = {
            'owner': name,
            'group': name,
            'content': '# bw managed',
        }
