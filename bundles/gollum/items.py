from shlex import quote

users = {
    'gollum': {
        'home': '/var/lib/gollum',
    }
}

directories = {
    '/opt/gollum': {
        'owner': 'gollum',
    },
    '/opt/gollum/.bundle': {
        'owner': 'gollum',
    },
    '/var/lib/gollum': {
        'owner': 'gollum',
    },
}

files = {
    '/opt/gollum/.bundle/config': {
        'content': 'BUNDLE_PATH: ".bundle/gems"',
    }
}

git_deploy = {
    '/opt/gollum': {
        'repo': 'https://github.com/gollum/gollum.git',
        'rev': f"v{node.metadata.get('gollum/version')}",
    },
    '/var/lib/gollum': {
        'repo': node.metadata.get('gollum/wiki'),
        'rev': 'main',
        'unless': 'test -e /var/lib/gollum/.git',
    },
}

def run(cmd):
    return f"su gollum -c " + quote(f"cd /opt/gollum && {cmd}")

actions = {
    'gollum_install_bundler': {
        'command': run("gem install bundler --user"),
        'unless': run("test -e $(ruby -e 'puts Gem.user_dir')/bin/bundle"),
        'needs': [
            'file:/opt/gollum/.bundle/config',
        ],
    },
    'gollum_bundle_install': {
        'command': run("$(ruby -e 'puts Gem.user_dir')/bin/bundle install"),
        'unless': run("$(ruby -e 'puts Gem.user_dir')/bin/bundle check"),
        'needs': [
            'git_deploy:/opt/gollum',
            'action:gollum_install_bundler',
        ],
    },
}

# TODO: AUTH
#https://github.com/bjoernalbers/gollum-auth
