for project, options in node.metadata.get('build-ci').items():
    directories[options['path']] = {
        'owner': 'build-ci',
        'group': options['group'],
        'mode': '770',
        'needs': [
            'user:build-ci',
        ],
    }
