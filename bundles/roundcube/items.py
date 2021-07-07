assert node.has_bundle('php')
assert node.has_bundle('mailserver')

directories = {
    '/opt/roundcube': {
        'owner': 'www-data',
    },
    '/opt/roundcube/logs': {
        'owner': 'www-data',
        'needs': [
            'git_deploy:/opt/roundcube',
        ],
    },
    '/opt/roundcube/temp': {
        'owner': 'www-data',
        'needs': [
            'git_deploy:/opt/roundcube',
        ],
    }
}

git_deploy['/opt/roundcube'] = {
    'repo': "https://github.com/roundcube/roundcubemail.git",
    'rev': node.metadata.get('roundcube/version'),
    'needs': [
        'directory:/opt/roundcube',
    ],
}

files['/opt/roundcube/config/config.inc.php'] = {
    'content_type': 'mako',
    'context': {
        'installer': node.metadata.get('roundcube/installer'),
        'product_name': node.metadata.get('roundcube/product_name'),
        'des_key': node.metadata.get('roundcube/des_key'),
        'database': node.metadata.get('roundcube/database'),
        'plugins': node.metadata.get('roundcube/plugins'),
    },
    'needs': [
        'git_deploy:/opt/roundcube',
    ],
}
