directories = {
    '/opt/rbenv': {},
    '/opt/rbenv/plugins': {
        'needs': [
            'git_deploy:/opt/rbenv',
        ],
    },
    '/opt/rbenv/plugins/ruby-build': {
        'needs': [
            'git_deploy:/opt/rbenv',
        ],
    },
}

git_deploy = {
    '/opt/rbenv': {
        'repo': 'https://github.com/sstephenson/rbenv.git',
        'rev': 'master',
    },
    '/opt/rbenv/plugins/ruby-build': {
        'repo': 'https://github.com/sstephenson/ruby-build.git',
        'rev': 'master',
        'needs': [
            'git_deploy:/opt/rbenv',
        ],
    },
}

for version in node.metadata.get('rbenv'):
    actions[f'install_ruby_{version}'] = {
        'command': f'RBENV_ROOT=/opt/rbenv /opt/rbenv/bin/rbenv install {version}',
        'unless': f'RBENV_ROOT=/opt/rbenv /opt/rbenv/bin/rbenv versions | cut -c 3- | cut -d" " -f1 | grep -q ^{version}$',
        'needs': [
            'git_deploy:/opt/rbenv',
            'git_deploy:/opt/rbenv/plugins/ruby-build',
            'pkg_apt:libyaml-dev',
        ],
    }


