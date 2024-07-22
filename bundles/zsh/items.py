from os.path import join

directories = {
    '/etc/zsh/oh-my-zsh': {},
    '/etc/zsh/oh-my-zsh/custom/plugins': {
        'mode': '0744',
        'needs': [
            f"git_deploy:/etc/zsh/oh-my-zsh",
        ]
    },
    '/etc/zsh/oh-my-zsh/custom/plugins/zsh-autosuggestions': {
        'mode': '0744',
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
    '/etc/zsh/zprofile': {
        'mode': '0744',
    },
    '/etc/zsh/oh-my-zsh/themes/bw.zsh-theme': {
        'mode': '0744',
        'needs': [
            f"git_deploy:/etc/zsh/oh-my-zsh",
        ]
    },
}

actions = {
    'chown_oh_my_zsh': {
        'command': 'chmod -R 744 /etc/zsh/oh-my-zsh',
        'triggered': True,
        'triggered_by': [
            "git_deploy:/etc/zsh/oh-my-zsh",
            "git_deploy:/etc/zsh/oh-my-zsh/custom/plugins/zsh-autosuggestions",
            "file:/etc/zsh/zprofile",
            "file:/etc/zsh/oh-my-zsh/themes/bw.zsh-theme",
        ],
    },
}

for name, user_config in node.metadata.get('users').items():
    if user_config.get('shell', None) == '/usr/bin/zsh':
        files[join(user_config['home'], '.zshrc')] = {
            'owner': name,
            'group': name,
            'content': '# bw managed',
        }
