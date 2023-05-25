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
