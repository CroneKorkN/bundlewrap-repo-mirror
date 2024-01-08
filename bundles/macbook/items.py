# brew install

actions['brew_install'] = {
    'command': '/opt/homebrew/bin/brew install ' + ' '.join(node.metadata.get('brew')),
    'unless': f"""PKGS=$(/opt/homebrew/bin/brew leaves); for p in {' '.join(node.metadata.get('brew'))}; do grep -q "$p" <<< $PKGS || exit 9; done"""
}

# bw init

directories['/Users/mwiegand/.config/bundlewrap/lock'] = {}

# home

files['/Users/mwiegand/.zshrc'] = {
    'source': 'zshrc',
    'mode': '0644',
}

# updater

files['/Users/mwiegand/.bin/macbook-update'] = {
    'mode': '755',
}

with open(f'{repo.path}/bundles/zsh/files/bw.zsh-theme') as f:
    files['/Users/mwiegand/.zsh/oh-my-zsh/themes/bw.zsh-theme'] = {
        'content': f.read(),
        'mode': '0644',
    }

# direnv

directories['/Users/mwiegand/.local/share/direnv'] = {}
files['/Users/mwiegand/.local/share/direnv/gnu'] = {}
files['/Users/mwiegand/.local/share/direnv/pyenv'] = {}
files['/Users/mwiegand/.local/share/direnv/venv'] = {}
files['/Users/mwiegand/.local/share/direnv/bundlewrap'] = {}


##################

for element in [*files.values(), *directories.values()]:
    element.update({
        'owner': 'mwiegand',
        'group': 'staff',
        **element,
    })
