# Items for the left4me bundle.
# Systemd units come from metadata via bundles/systemd/ — there are no
# .service or .slice files in this bundle's files/ tree.

directories = {
    '/opt/left4me': {
        'owner': 'left4me',
        'group': 'left4me',
    },
    '/etc/left4me': {
        'owner': 'root',
        'group': 'root',
        'mode': '0755',
    },
    '/var/lib/left4me': {
        # left4me's home dir — useradd creates with 0700; loosen to 0711 so
        # l4d2-sandbox can traverse (but not list) for bwrap bind-mounts.
        'owner': 'left4me',
        'group': 'left4me',
        'mode': '0711',
    },
    '/var/lib/left4me/installation':   {'owner': 'left4me', 'group': 'left4me'},
    '/var/lib/left4me/overlays':       {'owner': 'left4me', 'group': 'left4me'},
    '/var/lib/left4me/instances':      {'owner': 'left4me', 'group': 'left4me'},
    '/var/lib/left4me/runtime':        {'owner': 'left4me', 'group': 'left4me'},
    '/var/lib/left4me/workshop_cache': {'owner': 'left4me', 'group': 'left4me'},
    '/var/lib/left4me/tmp':            {'owner': 'left4me', 'group': 'left4me'},
    '/usr/local/libexec/left4me': {
        'owner': 'root',
        'group': 'root',
        'mode': '0755',
    },
}

groups = {
    'left4me':      {'gid': 980},
    'l4d2-sandbox': {'gid': 981},
}

users = {
    'left4me': {
        'uid': 980,
        'gid': 980,
        'home': '/var/lib/left4me',
        'shell': '/usr/sbin/nologin',
    },
    'l4d2-sandbox': {
        'uid': 981,
        'gid': 981,
        'shell': '/usr/sbin/nologin',
    },
}
# UIDs/GIDs pinned in the system-package range (100-999, per Debian
# policy) so file ownership is deterministic across rebuilds and
# backup restores. 980/981 are unused elsewhere in this repo.

# Privileged helpers (mode 0755 root:root). Listed by sudoers as the only
# commands left4me can invoke as root NOPASSWD.
HELPERS = (
    'left4me-systemctl',
    'left4me-journalctl',
    'left4me-overlay',
    'left4me-script-sandbox',
)

files = {
    **{
        f'/usr/local/libexec/left4me/{h}': {
            'source': f'usr/local/libexec/left4me/{h}',
            'mode': '0755',
            'owner': 'root',
            'group': 'root',
        }
        for h in HELPERS
    },
    '/etc/left4me/sandbox-resolv.conf': {
        'source': 'etc/left4me/sandbox-resolv.conf',
        'mode': '0644',
        'owner': 'root',
        'group': 'root',
    },
    '/etc/sudoers.d/left4me': {
        'source': 'etc/sudoers.d/left4me',
        'mode': '0440',
        'owner': 'root',
        'group': 'root',
        'test_with': 'visudo -cf {}',
    },
    '/etc/sysctl.d/99-left4me.conf': {
        'source': 'etc/sysctl.d/99-left4me.conf',
        'mode': '0644',
        'owner': 'root',
        'group': 'root',
        'triggers': [
            'action:left4me_sysctl_reload',
        ],
    },
    '/etc/left4me/host.env': {
        'source': 'etc/left4me/host.env.mako',
        'content_type': 'mako',
        'mode': '0644',
        'owner': 'root',
        'group': 'root',
    },
    '/etc/left4me/web.env': {
        'source': 'etc/left4me/web.env.mako',
        'content_type': 'mako',
        'mode': '0640',
        'owner': 'root',
        'group': 'left4me',
        'needs': [
            'group:left4me',
        ],
    },
}

actions = {
    'left4me_sysctl_reload': {
        'command': 'sysctl --system >/dev/null',
        'triggered': True,
    },
}

git_deploy = {
    '/opt/left4me/src': {
        'repo': node.metadata.get('left4me/git_url'),
        'rev': node.metadata.get('left4me/git_branch'),
        'triggers': [
            'action:left4me_create_venv',
            'action:left4me_pip_install',
        ],
    },
}

actions['left4me_create_venv'] = {
    'command': 'sudo -u left4me /usr/bin/python3 -m venv /opt/left4me/.venv',
    'unless':  'test -x /opt/left4me/.venv/bin/python',
    'cascade_skip': False,
    'needs': [
        'directory:/opt/left4me',
        'pkg_apt:python3-venv',
        'user:left4me',
    ],
    'triggers': [
        'action:left4me_pip_upgrade',
    ],
}

actions['left4me_pip_upgrade'] = {
    'command': 'sudo -u left4me /opt/left4me/.venv/bin/python -m pip install --upgrade pip',
    'triggered': True,
    'cascade_skip': False,
    'needs': [
        'pkg_apt:python3-pip',
    ],
    'triggers': [
        'action:left4me_pip_install',
    ],
}

actions['left4me_pip_install'] = {
    # Single pip invocation installs both editable packages from the same checkout.
    'command': 'sudo -u left4me /opt/left4me/.venv/bin/pip install -e /opt/left4me/src/l4d2host -e /opt/left4me/src/l4d2web',
    'triggered': True,
    'cascade_skip': False,
    'needs': [
        'git_deploy:/opt/left4me/src',
        'action:left4me_create_venv',
    ],
    'triggers': [
        'action:left4me_alembic_upgrade',
    ],
}

actions['left4me_alembic_upgrade'] = {
    # Mirrors deploy-test-server.sh:239-242. Runs as left4me with both env
    # files sourced; JOB_WORKER_ENABLED=false so a stray worker doesn't race
    # with the migration.
    'command': (
        'sudo -u left4me sh -c "'
        'cd /opt/left4me/src/l4d2web && '
        'set -a && . /etc/left4me/host.env && . /etc/left4me/web.env && set +a && '
        'env JOB_WORKER_ENABLED=false PYTHONPATH=/opt/left4me/src '
        '/opt/left4me/.venv/bin/alembic -c /opt/left4me/src/l4d2web/alembic.ini upgrade head'
        '"'
    ),
    'triggered': True,
    'cascade_skip': False,
    'needs': [
        'action:left4me_pip_install',
        'file:/etc/left4me/host.env',
        'file:/etc/left4me/web.env',
    ],
    'triggers': [
        'action:left4me_seed_overlays',
        'svc_systemd:left4me-web.service:restart',
    ],
}

actions['left4me_seed_overlays'] = {
    # Idempotent: refreshes script bodies in place; existing overlay rows keep their ids.
    'command': (
        'sudo -u left4me sh -c "'
        'set -a && . /etc/left4me/host.env && . /etc/left4me/web.env && set +a && '
        'env JOB_WORKER_ENABLED=false PYTHONPATH=/opt/left4me/src '
        '/opt/left4me/.venv/bin/flask --app l4d2web.app:create_app '
        'seed-script-overlays /opt/left4me/src/examples/script-overlays'
        '"'
    ),
    'triggered': True,
    'cascade_skip': False,
    'needs': [
        'action:left4me_alembic_upgrade',
    ],
}
