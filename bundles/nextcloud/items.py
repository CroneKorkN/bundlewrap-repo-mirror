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
actions['extract_nextcloud'] = {
    'command': f'tar xfvj /tmp/nextcloud-{version}.tar.bz2 --strip 1 -C /opt/nextcloud nextcloud',
    'unless': f"""php -r 'include "/opt/nextcloud/version.php"; echo "$OC_VersionString";' | grep -q '^{version}$'""",
    'preceded_by': [
        f'download:/tmp/nextcloud-{version}.tar.bz2',
    ],
    'needs': [
        'directory:/opt/nextcloud',
    ],
}

# DIRECTORIES

directories['/opt/nextcloud'] = {}
directories['/opt/nextcloud/config'] = {
    'owner': 'www-data',
    'group': 'www-data',
}
directories['/opt/nextcloud/apps'] = {
    'owner': 'www-data',
    'group': 'www-data',
}
directories['/var/lib/nextcloud'] = {
    'owner': 'www-data',
    'group': 'www-data',
    'mode': '0770',
}
actions['chown_/opt/nextcloud/apps'] = {
    'command': 'chown -R www-data:www-data /opt/nextcloud/apps',
    'unless': '! stat -c "%U:%G" /opt/nextcloud/apps/* | grep -vq www-data:www-data',
    'needs': [
        'action:extract_nextcloud',
    ],
}

# SETUP

files['/opt/nextcloud/config/config.php'] = {
    'content_type': 'any',
    'owner': 'www-data',
    'group': 'www-data',
    'mode': '640',
    'needs': [
        'action:extract_nextcloud',
    ],
}
files['/opt/nextcloud/config/managed.config.php'] = {
    'content_type': 'mako',
    'owner': 'www-data',
    'group': 'www-data',
    'mode': '640',
    'context': {
        'db_password': node.metadata.get('postgresql/roles/nextcloud/password'),
    },
    'needs': [
        'action:extract_nextcloud',
    ],
}
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
        'postgres_db:nextcloud',
        f"directory:/var/lib/nextcloud",
        'directory:/opt/nextcloud',
        'directory:/opt/nextcloud/config',
        'directory:/opt/nextcloud/apps',
        'action:chown_/opt/nextcloud/apps',
        'action:extract_nextcloud',
        'file:/opt/nextcloud/config/config.php',
        'file:/opt/nextcloud/config/managed.config.php',
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
    ],
}
