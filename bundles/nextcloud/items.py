assert node.has_bundle('php')

from shlex import quote
from os.path import join
from mako.template import Template

def occ(command, *args, **kwargs):
    return f"""sudo -u www-data php /opt/nextcloud/occ {command} {' '.join(args)} {' '.join(f'--{name.replace("_", "-")}' + (f'={value}' if value else '') for name, value in kwargs.items())}"""

version = node.metadata.get('nextcloud/version')

# FILES AND FOLDERS

downloads[f'/tmp/nextcloud-{version}.tar.bz2'] = {
    'url': f'https://download.nextcloud.com/server/releases/nextcloud-{version}.tar.bz2',
    'sha256': node.metadata.get('nextcloud/sha256'),
    'triggered': True,
}

directories['/opt/nextcloud'] = {}
directories['/opt/nextcloud/config'] = {
    'owner': 'www-data',
    'group': 'www-data',
}
directories['/opt/nextcloud/apps'] = {
    'owner': 'www-data',
    'group': 'www-data',
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

actions['chown_/opt/nextcloud/apps'] = {
    'command': 'chown -R www-data:www-data /opt/nextcloud/apps',
    'unless': '! stat -c "%U:%G" /opt/nextcloud/apps/* | grep -vq www-data:www-data',
    'needs': [
        'action:extract_nextcloud',
    ],
}
actions['chown_/opt/nextcloud/config'] = {
    'command': 'chown -R www-data:www-data /opt/nextcloud/config',
    'unless': '! stat -c "%U:%G" /opt/nextcloud/config/* | grep -vq www-data:www-data',
    'needs': [
        'action:extract_nextcloud',
    ],
}

directories[node.metadata.get('nextcloud/data_dir')] = {
    'owner': 'www-data',
    'group': 'www-data',
    'mode': '0770',
}

# SETUP

with open(join(repo.path, 'bundles', 'nextcloud', 'files', 'config.php')) as file:
    content = Template(file.read()).render(
        setup=True,
        instance_id=node.metadata.get('nextcloud/instance_id'),
    )
    actions['nextcloud_config_for_install'] = {
        'command': f'echo {quote(content)} > /opt/nextcloud/config/config.php && chown www-data:www-data /opt/nextcloud/config/config.php',
        'needs': [
            'action:extract_nextcloud',
        ],
        'triggered': True,
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
        data_dir=node.metadata.get('nextcloud/data_dir'),
    ),
    'unless': """
        psql -At -d nextcloud -c "SELECT 'OK' FROM information_schema.tables WHERE table_name='users' AND table_schema='public'" | grep -q "^OK$"
    """,
    'needs': [
        'postgres_db:nextcloud',
        f"directory:{node.metadata.get('nextcloud/data_dir')}",
        'directory:/opt/nextcloud',
        'directory:/opt/nextcloud/config',
        'directory:/opt/nextcloud/apps',
        'action:chown_/opt/nextcloud/config',
        'action:chown_/opt/nextcloud/apps',
        'action:extract_nextcloud',
    ],
    'preceded_by': [
        'action:nextcloud_config_for_install',
    ],
}

files['/opt/nextcloud/config/config.php'] = {
    'content_type': 'mako',
    'context': {
        'setup': False,
        'version': version,
        'instance_id': node.metadata.get('nextcloud/instance_id'),
        'db_password': node.metadata.get('postgresql/roles/nextcloud/password'),
    },
    'owner': 'www-data',
    'group': 'www-data',
    'mode': '0770',
    'needs': [
        'action:install_nextcloud',
    ],
}

# UPGRADE

actions['upgrade_nextcloud'] = {
    'command': occ('upgrade'),
    'unless': occ('status') + ' | grep -q "installed: true"',
    'needs': [
        'file:/opt/nextcloud/config/config.php',
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
