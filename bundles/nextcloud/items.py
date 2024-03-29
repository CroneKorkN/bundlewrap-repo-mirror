import json


assert node.has_bundle('php')

version = node.metadata.get('nextcloud/version')

directories = {
    '/opt/nextcloud': {},
    '/etc/nextcloud': {
        'owner': 'www-data',
        'group': 'www-data',
    },
    '/var/lib/nextcloud': {
        'owner': 'www-data',
        'group': 'www-data',
        'mode': '770',
    },
    '/var/lib/nextcloud/.userapps': {
        'owner': 'www-data',
        'group': 'www-data',
    },
    '/var/lib/nextcloud/.cache': {
        'owner': 'www-data',
        'group': 'www-data',
    },
}

downloads[f'/tmp/nextcloud-{version}.tar.bz2'] = {
    'url': f'https://download.nextcloud.com/server/releases/nextcloud-{version}.tar.bz2',
    'sha256_url': '{url}.sha256',
    'triggered': True,
}
actions['delete_nextcloud'] = {
    'command': 'rm -rf /opt/nextcloud/*',
    'triggered': True,
}
actions['extract_nextcloud'] = {
    'command': f'tar xfvj /tmp/nextcloud-{version}.tar.bz2 --strip 1 -C /opt/nextcloud nextcloud',
    'unless': f"""php -r 'include "/opt/nextcloud/version.php"; echo "$OC_VersionString";' | grep -q '^{version}$'""",
    'preceded_by': [
        'action:delete_nextcloud',
        f'download:/tmp/nextcloud-{version}.tar.bz2',
    ],
    'needs': [
        'directory:/opt/nextcloud',
    ],
}

symlinks = {
    '/opt/nextcloud/config': {
        'target': '/etc/nextcloud',
        'owner': 'www-data',
        'group': 'www-data',
        'needs': [
            'action:extract_nextcloud',
        ],
    },
    '/opt/nextcloud/userapps': {
        'target': '/var/lib/nextcloud/.userapps',
        'owner': 'www-data',
        'group': 'www-data',
        'needs': [
            'action:extract_nextcloud',
        ],
    },
}

files = {
    '/etc/nextcloud/managed.config.php': {
        'owner': 'www-data',
        'group': 'www-data',
        'mode': '640',
        'needs': [
            'directory:/etc/nextcloud',
        ],
    },
    '/etc/nextcloud/managed.config.json': {
        'content': json.dumps(node.metadata.get('nextcloud/config'), indent=4, sort_keys=True),
        'owner': 'www-data',
        'group': 'www-data',
        'mode': '640',
        'needs': [
            'directory:/etc/nextcloud',
        ],
    },}

# SETUP

actions['install_nextcloud'] = {
    'command': repo.libs.nextcloud.occ(
        'maintenance:install',
        no_interaction=None,
        database='pgsql',
        database_name='nextcloud',
        database_host='localhost',
        database_user='nextcloud',
        database_pass=node.metadata.get('postgresql/roles/nextcloud/password'),
        admin_user='admin',
        admin_pass=node.metadata.get('nextcloud/admin_pass'),
        data_dir='/var/lib/nextcloud',
    ),
    'unless': repo.libs.nextcloud.occ('status') + ' | grep -q "installed: true"',
    'needs': [
        'directory:/etc/nextcloud',
        'directory:/opt/nextcloud',
        'directory:/var/lib/nextcloud',
        'directory:/var/lib/nextcloud/.userapps',
        'directory:/var/lib/nextcloud/.cache',
        'symlink:/opt/nextcloud/config',
        'symlink:/opt/nextcloud/userapps',
        'action:extract_nextcloud',
        'file:/etc/nextcloud/managed.config.php',
        'postgres_db:nextcloud',
    ],
}

# UPGRADE

files['/opt/nextcloud_upgrade_status.php'] = {
    'source': 'upgrade_status.php',
    'owner': 'www-data',
    'group': 'www-data',
    'mode': '640',
    'needs': [
        'action:extract_nextcloud',
    ],
}

actions['upgrade_nextcloud'] = {
    'command': repo.libs.nextcloud.occ('upgrade'),
    'unless': 'sudo -u www-data php /opt/nextcloud_upgrade_status.php; test $? -ne 99',
    'needs': [
        'file:/opt/nextcloud_upgrade_status.php',
        'action:install_nextcloud',
    ],
}

actions['nextcloud_add_missing_inidces'] = {
    'command': repo.libs.nextcloud.occ('db:add-missing-indices'),
    'needs': [
        'action:upgrade_nextcloud',
    ],
    'triggered': True,
    'triggered_by': [
        f'action:extract_nextcloud',
    ],
}

# RESCAN

files['/opt/nextcloud_rescan'] = {
    'source': 'rescan',
    'owner': 'www-data',
    'group': 'www-data',
    'mode': '550',
    'needs': [
        'action:extract_nextcloud',
    ],
}
