assert node.has_bundle('php')

from shlex import quote
from os.path import join
from mako.template import Template

def occ(command, *args, **kwargs):
    return f"""sudo -u www-data php /opt/nextcloud/occ {command} {' '.join(args)} {' '.join(f'--{name.replace("_", "-")}' + (f'={value}' if value else '') for name, value in kwargs.items())}"""

version = node.metadata.get('nextcloud/version')

# DOWNLOAD

downloads[f'/tmp/nextcloud-{version}.tar.bz2'] = {
    'url': f'https://download.nextcloud.com/server/releases/nextcloud-{version}.tar.bz2',
    'sha256': node.metadata.get('nextcloud/sha256'),
    'triggered': True,
}
actions['delete_nextcloud'] = {
    'command': 'rm -rf /opt/nextcloud/*',
    'triggered': True,
}
actions['extract_nextcloud'] = {
    'command': f'tar xfvj /tmp/nextcloud-{version}.tar.bz2 --skip-old-files --strip 1 -C /opt/nextcloud nextcloud',
    'unless': f"""php -r 'include "/opt/nextcloud/version.php"; echo "$OC_VersionString";' | grep -q '^{version}$'""",
    'preceded_by': [
        'action:delete_nextcloud',
        f'download:/tmp/nextcloud-{version}.tar.bz2',
    ],
    'needs': [
        'action:symlink_/opt/nextcloud/config',
        'directory:/opt/nextcloud',
    ],
}

# DIRECTORIES, FILES AND SYMLINKS

directories['/etc/nextcloud'] = {
    'owner': 'www-data',
    'group': 'www-data',
}
directories['/opt/nextcloud'] = {}
directories['/var/lib/nextcloud'] = {
    'owner': 'www-data',
    'group': 'www-data',
    'mode': '770',
}
directories['/var/lib/nextcloud/.apps'] = {
    'owner': 'www-data',
    'group': 'www-data',
}
directories['/var/lib/nextcloud/.cache'] = {
    'owner': 'www-data',
    'group': 'www-data',
}
files['/etc/nextcloud/CAN_INSTALL'] = {
    'content': '',
    'owner': 'www-data',
    'group': 'www-data',
    'mode': '640',
    'needs': [
        'directory:/etc/nextcloud',
    ],
}
files['/etc/nextcloud/managed.config.php'] = {
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
}
actions['symlink_/opt/nextcloud/config'] = {
    'command': f'ln -s /etc/nextcloud /opt/nextcloud/config && chown www-data:www-data /opt/nextcloud/config',
    'unless': 'readlink /opt/nextcloud/config | grep -q /etc/nextcloud',
    'needs': [
        'action:delete_nextcloud',
        'directory:/etc/nextcloud',
    ],
}
actions['symlink_/opt/nextcloud/userapps'] = {
    'command': f'ln -s /var/lib/nextcloud/.apps /opt/nextcloud/userapps && chown www-data:www-data /opt/nextcloud/userapps',
    'unless': 'readlink /opt/nextcloud/userapps | grep -q /var/lib/nextcloud/.apps',
    'needs': [
        'action:delete_nextcloud',
        'directory:/var/lib/nextcloud/.apps',
    ],
}

# SETUP

actions['install_nextcloud'] = {
    'command': occ(
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
    'unless': occ('status') + ' | grep -q "installed: true"',
    'needs': [
        'directory:/etc/nextcloud',
        'directory:/opt/nextcloud',
        'directory:/var/lib/nextcloud',
        'directory:/var/lib/nextcloud/.apps',
        'directory:/var/lib/nextcloud/.cache',
        'file:/etc/nextcloud/CAN_INSTALL',
        'file:/etc/nextcloud/managed.config.php',
        'action:extract_nextcloud',
        'action:symlink_/opt/nextcloud/userapps',
        'action:symlink_/opt/nextcloud/config',
        'postgres_db:nextcloud',
    ],
}

# UPGRADE

actions['upgrade_nextcloud'] = {
    'command': occ('upgrade'),
    'unless': occ('status') + f' | grep -q "versionstring: {version}"',
    'needs': [
        'action:install_nextcloud',
    ],
}

actions['nextcloud_add_missing_inidces'] = {
    'command': occ('db:add-missing-indices'),
    'needs': [
        'action:upgrade_nextcloud',
    ],
    'triggered': True,
    'triggered_by': [
        f'action:extract_nextcloud',
        f'action:upgrade_nextcloud',
    ],
}
