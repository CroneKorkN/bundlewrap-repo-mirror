from os.path import join

files = {
    '/etc/zsh/zprofile': {
        'mode': '0644',
    },
}

# Empty stub in each zsh user's home. zsh-newuser-install fires on login
# when none of ~/.{zshrc,zshenv,zprofile,zlogin} exists, and the real
# config lives in /etc/zsh/zprofile — so we keep a one-line marker file
# here to suppress the new-user wizard.
for name, user_config in node.metadata.get('users').items():
    if user_config.get('shell', None) == '/usr/bin/zsh':
        files[join(user_config['home'], '.zshrc')] = {
            'owner': name,
            'group': name,
            'content': '# bw managed; real config in /etc/zsh/zprofile\n',
        }
