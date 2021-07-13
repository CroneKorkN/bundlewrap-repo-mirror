from os.path import join

for name, user_config in node.metadata.get('users').items():
    if user_config.get('shell', None) != '/usr/bin/zsh':
        continue

    directories = {
        join(user_config['home'], '.zsh'): {
            'owner': name,
        },
        join(user_config['home'], '.zsh/oh-my-zsh'): {
            'owner': name,
        },
        join(user_config['home'], '.zsh/oh-my-zsh/custom/plugins/zsh-autosuggestions'): {
            'owner': name,
            'needs': {
                f"git_deploy:{join(user_config['home'], '.zsh/oh-my-zsh')}",
            },
        },
    }
    
    
    git_deploy = {
        join(user_config['home'], '.zsh/oh-my-zsh'): {
            'repo': 'git://github.com/ohmyzsh/ohmyzsh.git',
            'rev': 'master',
        },
        join(user_config['home'], '.zsh/oh-my-zsh/custom/plugins/zsh-autosuggestions'): {
            'repo': 'git://github.com/zsh-users/zsh-autosuggestions.git',
            'rev': 'master',
        },
    }

    files = {
        join(user_config['home'], '.zshrc'): {
            'owner': name,
            'source': 'zshrc',
        },
        join(user_config['home'], '.zsh/oh-my-zsh/themes/bw.zsh-theme'): {
            'owner': name,
            'needs': {
                f"git_deploy:{join(user_config['home'], '.zsh/oh-my-zsh')}",
            },
        },
    }
    
