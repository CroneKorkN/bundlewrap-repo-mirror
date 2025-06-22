directories = {
    '/var/www/yourls/htdocs': {
        'owner': 'www-data',
        'group': 'www-data',
        'mode': '0755',
    },

    # FIXME:
    '/var/www/certbot': {
        'owner': 'www-data',
        'group': 'www-data',
        'mode': '0755',
    }
}

git_deploy = {
    '/var/www/yourls/htdocs': {
        'repo': 'https://github.com/YOURLS/YOURLS.git',
        'rev': node.metadata.get('yourls/version'),
        'needs': [
            'directory:/var/www/yourls/htdocs',
        ],
        'triggers': [
            'svc_systemd:nginx:restart',
        ],
    },
}

files = {
    f'/var/www/yourls/htdocs/user/config.php': {
        'content_type': 'mako',
        'mode': '0440',
        'owner': 'www-data',
        'group': 'www-data',
        'context': {
            'db_password': node.metadata.get('mariadb/databases/yourls/password'),
            'hostname': node.metadata.get('yourls/hostname'),
            'cookiekey': node.metadata.get('yourls/cookiekey'),
            'users': node.metadata.get('yourls/users'),
        },
        'needs': [
            'git_deploy:/var/www/yourls/htdocs',
        ],
        'triggers': [
            'svc_systemd:nginx:restart',
        ],
    },
}
