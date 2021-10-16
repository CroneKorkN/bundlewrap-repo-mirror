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

files = {
    '/etc/rspamd/local.d/ip_whitelist.map': {
        'content': '\n'.join(
            sorted(node.metadata.get('rspamd/ip_whitelist'))
        ) + '\n',
        'triggers': {
            'svc_systemd:rspamd:restart',
        },
    },
    '/etc/rspamd/local.d/worker-controller.inc': {
        'content_type': 'mako',
        'triggers': {
            'svc_systemd:rspamd:restart',
        },
    }
}

local_config_path = join(repo.path, 'bundles', 'rspamd', 'files', 'local.d')
for f in listdir(local_config_path):
    files[f'/etc/rspamd/local.d/{f}'] = {
        'source': f'local.d/{f}',
        'triggers': {
            'svc_systemd:rspamd:restart',
        },
    }

override_config_path = join(repo.path, 'bundles', 'rspamd', 'files', 'override.d')
for f in listdir(override_config_path):
    files[f'/etc/rspamd/override.d/{f}'] = {
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
}
