assert node.has_bundle('php')
assert node.has_bundle('mailserver')

version = node.metadata.get('roundcube/version')

directories = {
    '/opt/roundcube': {
        'owner': 'www-data',
    },
    '/opt/roundcube/logs': {
        'owner': 'www-data',
        'needs': [
            'action:extract_roundcube',
        ],
    },
    '/opt/roundcube/temp': {
        'owner': 'www-data',
        'needs': [
            'action:extract_roundcube',
        ],
    }
}


downloads[f'/tmp/roundcube-{version}.tar.gz'] = {
    'url': f'https://github.com/roundcube/roundcubemail/releases/download/{version}/roundcubemail-{version}-complete.tar.gz',
    'gpg_signature_url': '{url}.asc',
    'gpg_pubkey_url': 'https://roundcube.net/download/pubkey.asc',
    'triggered': True,
}
actions['delete_roundcube'] = {
    'command': 'rm -rf /opt/roundcube/*',
    'triggered': True,
}
actions['extract_roundcube'] = {
    'command': f'tar xfvz /tmp/roundcube-{version}.tar.gz --strip 1 -C /opt/roundcube',
    'unless': f'grep -q "Version {version}" /opt/roundcube/index.php',
    'preceded_by': [
        'action:delete_roundcube',
        f'download:/tmp/roundcube-{version}.tar.gz',
    ],
    'needs': [
        'directory:/opt/roundcube',
    ],
    'triggers': [
        'action:chown_roundcube',
        'action:composer_install',
    ],
}
actions['chown_roundcube'] = {
    'command': 'chown -R www-data /opt/roundcube',
    'triggered': True,
}


files = {
    '/opt/roundcube/config/config.inc.php': {
        'content_type': 'mako',
        'context': {
            'installer': node.metadata.get('roundcube/installer'),
            'product_name': node.metadata.get('roundcube/product_name'),
            'des_key': node.metadata.get('roundcube/des_key'),
            'database': node.metadata.get('roundcube/database'),
            'plugins': node.metadata.get('roundcube/plugins'),
        },
        'needs': [
            'action:chown_roundcube',
        ],
    },
    '/opt/roundcube/plugins/password/config.inc.php': {
        'source': 'password.config.inc.php',
        'content_type': 'mako',
        'context': {
            'mailserver_db_password': node.metadata.get('mailserver/database/password'),
        },
        'needs': [
            'action:chown_roundcube',
        ],
    },
}

actions['composer_install'] = {
    'command': "cp /opt/roundcube/composer.json-dist /opt/roundcube/composer.json && su www-data -s /bin/bash -c '/usr/bin/composer -d /opt/roundcube install'",
    'triggered': True,
    'needs': [
        'action:chown_roundcube',
    ],
}
