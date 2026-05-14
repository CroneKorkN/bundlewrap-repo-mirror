# Items for the left4me bundle.
# Systemd units come from metadata via bundles/systemd/ — there are no
# .service or .slice files in this bundle's files/ tree. Cpuset drop-ins
# for system.slice / user.slice are likewise emitted via systemd/units
# in metadata.py (key: '<parent>.d/<basename>.conf').

directories = {
    '/opt/left4me': {
        'owner': 'left4me',
        'group': 'left4me',
    },
    '/opt/left4me/src': {
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
    '/opt/left4me/steam':              {'owner': 'left4me', 'group': 'left4me'},
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

# Privileged helpers are installed by the `install_left4me_scripts`
# action (below) directly from the left4me git checkout — no verbatim
# copy in this bundle's files/ tree. Sudoers (further below) lists the
# specific paths that left4me may invoke as root NOPASSWD.

files = {
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
        'mode': '0640',
        'owner': 'root',
        # group=left4me so the alembic + seed-overlays actions (which run as
        # `sudo -u left4me sh -c '. /etc/left4me/host.env'`) can source it.
        # Same pattern as web.env below.
        'group': 'left4me',
        'needs': [
            'group:left4me',
        ],
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
    'left4me_dpkg_add_i386_arch': {
        # steamcmd is 32-bit and pulls libc6:i386 + lib32z1 from the i386 arch.
        # apt-get update is part of this action because newly-added foreign
        # archs need a fresh package list before any :i386 package resolves.
        'command': 'dpkg --add-architecture i386 && apt-get update',
        'unless': 'dpkg --print-foreign-architectures | grep -qx i386',
        'cascade_skip': False,
    },
    'left4me_install_steamcmd': {
        # Steam's tarball is rolling with no published checksum, so we can't
        # use download: (which requires a hash). Guard with a presence check
        # on steamcmd.sh — steamcmd self-updates at runtime, so chasing the
        # tarball version from bw isn't useful.
        'command': (
            'sudo -u left4me sh -c "'
            'cd /opt/left4me/steam && '
            'curl -fsSL https://media.steampowered.com/installer/steamcmd_linux.tar.gz | '
            'tar -xz'
            '"'
        ),
        'unless': 'test -x /opt/left4me/steam/steamcmd.sh',
        'cascade_skip': False,
        'needs': [
            'directory:/opt/left4me/steam',
            'pkg_apt:curl',
            'pkg_apt:libc6_i386',  # bw pkg_apt convention: _ → :
            'pkg_apt:lib32z1',
            'user:left4me',
        ],
    },
}

# steamcmd is invoked by absolute path (LEFT4ME_STEAMCMD in host.env),
# not via PATH lookup — see l4d2host/cli.py:install. We don't need to put
# anything in /usr/local/bin for it.

git_deploy = {
    '/opt/left4me/src': {
        'repo': node.metadata.get('left4me/git_url'),
        'rev': node.metadata.get('left4me/git_branch'),
        'triggers': [
            # On a code-update apply, refresh the DB schema. pip_install
            # would have triggered alembic in the create_venv path, but on
            # a normal apply pip_install's `unless` skips (packages still
            # importable from the previous editable install), and that
            # would leave alembic_upgrade dormant. Wiring git_deploy →
            # alembic directly ensures new migrations land whenever new
            # code lands. alembic upgrade head is idempotent (no-op when
            # already at head), so this is safe to fire on every code
            # update; the seed_overlays + service:restart cascade off
            # alembic also covers picking up the new code in gunicorn.
            'action:left4me_alembic_upgrade',
            # Privileged-helper scripts: reinstall from the new checkout
            # into /usr/local/{libexec,sbin}/ as root-owned. No-op when
            # the checkout didn't actually change (action is triggered).
            'action:install_left4me_scripts',
        ],
        # chown_src and pip_install are NOT in triggers — they run every
        # apply gated by their own `unless` guards, which makes the chain
        # self-healing after a partial failure. (Items in a triggers list
        # must be triggered:True, which would lose that property.)
    },
}

actions['install_left4me_scripts'] = {
    # Copy privileged scripts from the deployed left4me checkout into
    # /usr/local/{libexec,sbin}/ as root:root 0755. Source of truth for
    # the file content is left4me's deploy/files/usr/local/ tree; this
    # bundle no longer carries verbatim duplicates. The two install
    # globs map source dirs 1:1 to deploy targets. Triggered only on
    # git_deploy updates so a no-op apply doesn't re-copy.
    'command': (
        'install -m 0755 -o root -g root -t /usr/local/libexec/left4me/ '
        '/opt/left4me/src/deploy/files/usr/local/libexec/left4me/*; '
        'install -m 0755 -o root -g root -t /usr/local/sbin/ '
        '/opt/left4me/src/deploy/files/usr/local/sbin/*'
    ),
    'triggered': True,
    'cascade_skip': False,
    'needs': [
        'git_deploy:/opt/left4me/src',
        'directory:/usr/local/libexec/left4me',
    ],
}

actions['left4me_chown_src'] = {
    # Runs every apply (cheap — chown -R on a small tree). Self-heals
    # whenever git_deploy extracts a new tarball as root-owned files.
    # Not in any triggers list so doesn't need triggered:True.
    'command': 'chown -R left4me:left4me /opt/left4me/src',
    'unless': 'test -z "$(find /opt/left4me/src \\! -user left4me -print -quit 2>/dev/null)"',
    'cascade_skip': False,
    'needs': [
        'git_deploy:/opt/left4me/src',
        'user:left4me',
        'group:left4me',
    ],
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
    # No triggers — pip_install runs on every apply (gated by `unless`)
    # rather than being chained from here. Keeps pip_upgrade scoped to
    # exactly its purpose.
}

actions['left4me_pip_install'] = {
    # Single pip invocation installs both editable packages from the same
    # checkout. Runs on every apply: pip install -e is fast on no-op, and
    # any gate weaker than "egg-info matches pyproject.toml" can mask
    # script regeneration — e.g. adding [project.scripts] later wouldn't
    # be picked up if `unless` only checks importability.
    'command': 'sudo -u left4me /opt/left4me/.venv/bin/pip install -e /opt/left4me/src/l4d2host -e /opt/left4me/src/l4d2web',
    'cascade_skip': False,
    'needs': [
        'git_deploy:/opt/left4me/src',
        'action:left4me_create_venv',
        'action:left4me_chown_src',
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
