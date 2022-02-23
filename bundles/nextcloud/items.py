assert node.has_bundle('php')

from shlex import quote
from os.path import join
from mako.template import Template

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
        'content_type': 'mako',
        'owner': 'www-data',
        'group': 'www-data',
        'mode': '640',
        'context': {
            'db_password': node.metadata.get('postgresql/roles/nextcloud/password'),
        },
        'needs': [
            'directory:/etc/nextcloud',
        ],
    },
    '/opt/nextcloud/rescan': {
        'owner': 'www-data',
        'group': 'www-data',
        'mode': '550',
        'needs': [
            'directory:/opt/nextcloud',
            'action:extract_nextcloud',
        ],
    },
}

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
    'unless': repo.libs.nextcloud.occ('status', output='json') + ' | jq -r .installed | grep -q "^true$"',
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

actions['upgrade_nextcloud'] = {
    'command': repo.libs.nextcloud.occ('upgrade'),
    'unless': "! " + repo.libs.nextcloud.occ('status') + ' | grep -q "Nextcloud or one of the apps require upgrade"',
    'needs': [
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
