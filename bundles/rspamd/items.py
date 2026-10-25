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

svc_systemd = {
    'rspamd': {
        'needs': {
            'pkg_apt:rspamd',
            # rspamd uploads its lua scripts to redis at startup only: start and restart it after redis.
            # a restart action that is not triggered does not skip this, triggered items never cascade
            'svc_systemd:redis-server',
            'svc_systemd:redis-server:restart',
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

# for the redis socket
actions['rspamd_redis_group'] = {
    'command': 'usermod -aG redis _rspamd',
    'unless': 'id -nG _rspamd | grep -qw redis',
    'needs': [
        'pkg_apt:rspamd',
        'pkg_apt:redis-server',
    ],
    'triggers': [
        'svc_systemd:rspamd:restart',
    ],
}

# a restarted redis has lost the uploaded scripts, so rspamd has to follow
actions['rspamd_restart_after_redis'] = {
    'command': 'systemctl restart rspamd',
    'triggered': True,
    'triggered_by': [
        'svc_systemd:redis-server:restart',
    ],
    'needs': [
        'svc_systemd:rspamd',
    ],
}
