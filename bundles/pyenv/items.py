from shlex import quote

directories = {
    '/opt/pyenv': {},
    '/opt/pyenv/install': {},
}

git_deploy = {
    '/opt/pyenv/install': {
        'repo': 'https://github.com/pyenv/pyenv.git',
        'rev': 'master',
        'needs': {
            'directory:/opt/pyenv/install',
        },
    },
}

for version in node.metadata.get('pyenv/versions'):
    actions[f'pyenv_install_{version}'] = {
        'command': f'PYENV_ROOT=/opt/pyenv /opt/pyenv/install/bin/pyenv install {quote(version)}',
        'unless': f'PYENV_ROOT=/opt/pyenv /opt/pyenv/install/bin/pyenv versions --bare | grep -Fxq {quote(version)}',
        'needs': {
            'git_deploy:/opt/pyenv/install',
        },
    }
