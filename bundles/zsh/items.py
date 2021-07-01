from os.path import join

for name, user_config in node.metadata.get('users').items():
    print(user_config)
    if 'oh_my_zsh' in user_config:
        directories = {
            join(user_config['home'], '.zsh'): {},
            join(user_config['home'], '.zsh/oh-my-zsh'): {},
        }
        
        git_deploy[join(user_config['home'], '.zsh/oh-my-zsh')] = {
            'repo': 'git://github.com/ohmyzsh/ohmyzsh.git',
            'rev': 'master',
        }
