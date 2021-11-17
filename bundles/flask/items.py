for name, conf in node.metadata.get('flask').items():
    for dep in conf.get('apt_dependencies', []):
        pkg_apt[dep] = {
            'needed_by': {
                f'svc_systemd:{name}',
            },
        }

    directories[f'/opt/{name}'] = {
        'owner': conf['user'],
        'group': conf['group'],
    }
    directories[f'/opt/{name}/src'] = {}

    git_deploy[f'/opt/{name}/src'] = {
        'repo': conf['git_url'],
        'rev': conf.get('git_branch', 'master'),
        'triggers': [
            f'action:flask_{name}_pip_install_deps',
            *conf.get('deployment_triggers', []),
        ],
    }

    # CONFIG

    env = conf.get('env', {})

    if conf.get('json_config', {}):
        env['APP_CONFIG'] = f'/opt/{name}/config.json'
        files[env['APP_CONFIG']] = {
            'source': 'flask.cfg',
            'context': {
                'json_config': conf.get('json_config', {}),
            },
        }

    if 'APP_CONFIG' in env:
        files[env['APP_CONFIG']].update({
            'content_type': 'mako',
            'group': 'www-data',
            'needed_by': [
                f'svc_systemd:{name}',
            ],
            'triggers': [
                f'svc_systemd:{name}:restart',
            ],
        })

    # secrets

    if 'secrets.json' in conf:
        env['APP_SECRETS'] = f'/opt/{name}/secrets.json'
        files[env['APP_SECRETS']] = {
            'content': conf['secrets.json'],
            'mode': '0600',
            'owner': conf.get('user', 'www-data'),
            'group': conf.get('group', 'www-data'),
            'needed_by': [
                f'svc_systemd:{name}',
            ],
        }

    # VENV

    actions[f'flask_{name}_create_virtualenv'] = {
        'cascade_skip': False,
        'command': f'python3 -m venv /opt/{name}/venv',
        'unless': f'test -d /opt/{name}/venv',
        'needs': [
            f'directory:/opt/{name}',
            'pkg_apt:python3-venv',
        ],
        'triggers': [
            f'action:flask_{name}_pip_install_deps',
        ],
    }

    actions[f'flask_{name}_pip_install_deps'] = {
        'cascade_skip': False,
        'command': f'/opt/{name}/venv/bin/pip3 install -r /opt/{name}/src/requirements-frozen.txt || /opt/{name}/venv/bin/pip3 install -r /opt/{name}/src/requirements.txt',
        'triggered': True, # TODO: https://stackoverflow.com/questions/16294819/check-if-my-python-has-all-required-packages
        'needs': [
            f'git_deploy:/opt/{name}/src',
            'pkg_apt:python3-pip',
        ],
        'triggers': [
            f'action:flask_{name}_pip_install_gunicorn',
        ],
    }

    actions[f'flask_{name}_pip_install_gunicorn'] = {
        'command': f'/opt/{name}/venv/bin/pip3 install -U gunicorn',
        'triggered': True,
        'cascade_skip': False,
        'needs': [
            f'action:flask_{name}_create_virtualenv',
        ],
        'triggers': [
            f'action:flask_{name}_pip_install',
        ],
    }

    actions[f'flask_{name}_pip_install'] = {
        'command': f'/opt/{name}/venv/bin/pip3 install -e /opt/{name}/src',
        'triggered': True,
        'cascade_skip': False,
        'triggers': [
            f'svc_systemd:{name}:restart',
        ],
    }

    # UNIT

    svc_systemd[name] = {
        'needs': [
            f'action:flask_{name}_pip_install',
            f'file:/etc/systemd/system/{name}.service',
        ],
    }
