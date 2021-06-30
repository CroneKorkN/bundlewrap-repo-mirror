assert node.has_bundle('php')

from shlex import quote
from os.path import join
from mako.template import Template

print(f"v{node.metadata.get('nextcloud/version')}")


directories = {
    '/opt/nextcloud': {},
    '/etc/nextcloud': {
        'owner': 'www-data',
    },
    '/var/lib/nextcloud': {
        'owner': 'www-data',
        'mode': '770',
    },
    '/var/lib/nextcloud/.apps': {
        'owner': 'www-data',
    },
    '/var/lib/nextcloud/.cache': {
        'owner': 'www-data',
    },
}

git_deploy = {
    '/opt/nextcloud': {
        'repo': 'git://github.com/nextcloud/server.git',
        'rev': f"v{node.metadata.get('nextcloud/version')}",
        'needs': {
            'directory:/opt/nextcloud',
        },
    },
    '/opt/nextcloud/3rdparty': {
        'repo': 'git://github.com/nextcloud/3rdparty.git',
        'rev': f"v{node.metadata.get('nextcloud/version')}",
        'needs': {
            'git_deploy:/opt/nextcloud',
        },
    },
}

symlinks = {
    '/opt/nextcloud/config': {
        'target': '/etc/nextcloud',
        'owner': 'www-data',
        'needs': [
            'git_deploy:/opt/nextcloud',
        ],
    },
    '/opt/nextcloud/userapps': {
        'target': '/var/lib/nextcloud/.apps',
        'owner': 'www-data',
        'needs': [
            'git_deploy:/opt/nextcloud',
        ],
    },
}

files = {
    '/etc/nextcloud/CAN_INSTALL': {
        'content': '',
        'owner': 'www-data',
        'mode': '640',
        'needs': [
            'directory:/etc/nextcloud',
        ],
    },
    '/etc/nextcloud/managed.config.php': {
        'content_type': 'mako',
        'owner': 'www-data',
        'mode': '640',
        'context': {
            'db_password': node.metadata.get('postgresql/roles/nextcloud/password'),
        },
        'needs': [
            'directory:/etc/nextcloud',
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
    'unless': repo.libs.nextcloud.occ('status') + ' | grep -q "installed: true"',
    'needs': [
        'directory:/etc/nextcloud',
        'directory:/opt/nextcloud',
        'directory:/var/lib/nextcloud',
        'directory:/var/lib/nextcloud/.apps',
        'directory:/var/lib/nextcloud/.cache',
        'symlink:/opt/nextcloud/config',
        'symlink:/opt/nextcloud/userapps',
        'git_deploy:/opt/nextcloud',
        'git_deploy:/opt/nextcloud/3rdparty',
        'file:/etc/nextcloud/CAN_INSTALL',
        'file:/etc/nextcloud/managed.config.php',
        'postgres_db:nextcloud',
    ],
}

# UPGRADE

actions['upgrade_nextcloud'] = {
    'command': repo.libs.nextcloud.occ('upgrade'),
    'unless': repo.libs.nextcloud.occ('status') + f' | grep -q "versionstring: {node.metadata.get("nextcloud/version")}"',
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
        f'git_deploy:/opt/nextcloud',
    ],
}
