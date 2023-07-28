from os import listdir
from os.path import join

repo.libs.tools.require_bundle(node, 'redis', 'rspamd does not work without a redis cache')

directories = {
    '/etc/rspamd/local.d': {
        'purge': True,
        'needs': {
            'pkg_apt:rspamd',
        },
        'triggers': {
            'svc_systemd:rspamd:restart',
        },
    },
    '/etc/rspamd/override.d': {
        'purge': True,
        'needs': {
            'pkg_apt:rspamd',
        },
        'triggers': {
            'svc_systemd:rspamd:restart',
        },
    },
}

for f in listdir(join(f'{repo.path}/bundles/rspamd/files/local.d')):
    files[f'/etc/rspamd/local.d/{f}'] = {
        'content_type': 'mako',
        'source': f'local.d/{f}',
        'triggers': {
            'svc_systemd:rspamd:restart',
        },
    }

for f in listdir(join(f'{repo.path}/bundles/rspamd/files/override.d')):
    files[f'/etc/rspamd/override.d/{f}'] = {
        'content_type': 'mako',
        'source': f'override.d/{f}',
        'triggers': {
            'svc_systemd:rspamd:restart',
        },
    }

svc_systemd = {
    'rspamd': {
        'needs': {
            'pkg_apt:rspamd',
        },
    },
    # FIXME: broken since debian 12
    'clamav-clamonacc': {
        'enabled': False,
        'running': False,
        'needs': {
            'pkg_apt:clamav',
        },
    },
}

actions = {
    'rspamd_configtest': {
        'command': 'false',
        'unless': 'rspamadm configtest',
        'needs': {
            'svc_systemd:rspamd',
        },
    },
}
