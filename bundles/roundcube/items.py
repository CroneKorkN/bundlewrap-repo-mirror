assert node.has_bundle('php')
assert node.has_bundle('mailserver')

roundcube_version = node.metadata.get('roundcube/version')
php_version = node.metadata.get('php/version')

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


files[f'/tmp/roundcube-{roundcube_version}.tar.gz'] = {
    'content_type': 'download',
    'source': f'https://github.com/roundcube/roundcubemail/releases/download/{roundcube_version}/roundcubemail-{roundcube_version}-complete.tar.gz',
    'triggered': True,
}
actions['delete_roundcube'] = {
    'command': 'rm -rf /opt/roundcube/*',
    'triggered': True,
}
actions['extract_roundcube'] = {
    'command': f'tar xfvz /tmp/roundcube-{roundcube_version}.tar.gz --strip 1 -C /opt/roundcube',
    'unless': f'grep -q "Version {roundcube_version}" /opt/roundcube/index.php',
    'preceded_by': [
        'action:delete_roundcube',
        f'file:/tmp/roundcube-{roundcube_version}.tar.gz',
    ],
    'needs': [
        'directory:/opt/roundcube',
    ],
    'triggers': [
        'action:chown_roundcube',
        'action:composer_lock_reset',
    ],
}
actions['chown_roundcube'] = {
    'command': 'chown -R www-data /opt/roundcube',
    'triggered': True,
}


files['/opt/roundcube/config/config.inc.php'] = {
    'content_type': 'mako',
    'context': {
        'installer': node.metadata.get('roundcube/installer'),
        'product_name': node.metadata.get('roundcube/product_name'),
        'des_key': node.metadata.get('roundcube/des_key'),
        'database': node.metadata.get('roundcube/database'),
        'plugins': node.metadata.get('roundcube/plugins'),
        'imap_host': node.metadata.get('mailserver/hostname'),
    },
    'needs': [
        'action:chown_roundcube',
    ],
    'triggers': [
        f'svc_systemd:php{php_version}-fpm.service:restart',
    ],
}
files['/opt/roundcube/plugins/password/config.inc.php'] = {
    'source': 'password.config.inc.php',
    'content_type': 'mako',
    'context': {
        'mailserver_db_password': node.metadata.get('mailserver/database/password'),
    },
    'needs': [
        'action:chown_roundcube',
    ],
}
actions['composer_lock_reset'] = {
    'command': 'rm /opt/roundcube/composer.lock',
    'triggered': True,
    'needs': [
        'action:chown_roundcube',
    ],
    'triggers': [
        'action:composer_install',
    ],
}
actions['composer_install'] = {
    'command': "cp /opt/roundcube/composer.json-dist /opt/roundcube/composer.json && su www-data -s /bin/bash -c '/usr/bin/composer -d /opt/roundcube install'",
    'triggered': True,
    'needs': [
        'action:chown_roundcube',
    ],
}
