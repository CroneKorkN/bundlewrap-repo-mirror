# Items for the left4me bundle.
# Systemd units come from metadata via bundles/systemd/ — there are no
# .service or .slice files in this bundle's files/ tree. Cpuset drop-ins
# for system.slice / user.slice are likewise emitted via systemd/units
# in metadata.py (key: '<parent>.d/<basename>.conf').

directories = {
    '/opt/left4me': {
        # Deploy-artifact root. Only /opt/left4me/src lives here; runtime
        # state (.venv, steamcmd) lives under /var/lib/left4me/. Root-owned
        # so left4me cannot drop new files alongside src/ (e.g. an attacker
        # with web-compromise can't plant a 'scripts.d/' loaded by future
        # deploy logic).
        'owner': 'root',
        'group': 'root',
        'mode': '0755',
    },
    '/opt/left4me/src': {
        # Source checkout. Root-owned because the production install model
        # is non-editable: pip_install copies the source to a left4me-owned
        # tempdir before building, so the source tree on disk is never
        # mutated at runtime and left4me only needs read access (which
        # world-readable bits provide). Keeps left4me from being able to
        # rewrite its own future hardening drop-ins / unit files under
        # /opt/left4me/src/deploy/ (target-side symlink model in the
        # deployment-responsibility reshape).
        'owner': 'root',
        'group': 'root',
    },
    '/etc/left4me': {
        'owner': 'root',
        'group': 'root',
        'mode': '0755',
    },
    '/var/lib/left4me': {
        # left4me's home dir — useradd creates with 0700; loosen to 0755 so
        # the systemd-imposed FS view for transient script-sandbox units
        # (running as left4me with TemporaryFileSystem=/var/lib + selective
        # binds) can traverse on its way to the overlay bind targets.
        'owner': 'left4me',
        'group': 'left4me',
        'mode': '0755',
    },
    '/var/lib/left4me/installation':   {'owner': 'left4me', 'group': 'left4me'},
    '/var/lib/left4me/overlays':       {'owner': 'left4me', 'group': 'left4me'},
    '/var/lib/left4me/instances':      {'owner': 'left4me', 'group': 'left4me'},
    '/var/lib/left4me/runtime':        {'owner': 'left4me', 'group': 'left4me'},
    '/var/lib/left4me/workshop_cache': {'owner': 'left4me', 'group': 'left4me'},
    '/var/lib/left4me/tmp':            {'owner': 'left4me', 'group': 'left4me'},
    '/var/lib/left4me/steam':          {'owner': 'left4me', 'group': 'left4me'},
    # Note: the venv (/var/lib/left4me/.venv) is created by the
    # left4me_create_venv action; declaring it here too would race with
    # `python -m venv` which expects to create the directory itself.
    '/usr/local/libexec/left4me': {
        'owner': 'root',
        'group': 'root',
        'mode': '0755',
    },
}

groups = {
    'left4me': {'gid': 980},
}

users = {
    'left4me': {
        'uid': 980,
        'gid': 980,
        'home': '/var/lib/left4me',
        'shell': '/usr/sbin/nologin',
    },
}
# UID/GID pinned in the system-package range (100-999, per Debian
# policy) so file ownership is deterministic across rebuilds and
# backup restores. 980 is unused elsewhere in this repo.
# (981 — formerly l4d2-sandbox — was collapsed into 980 on 2026-05-15;
# see left4me/docs/superpowers/plans/2026-05-15-uid-collapse.md.)

# Privileged helpers are installed by the `install_left4me_scripts`
# action (below) directly from the left4me git checkout at
# `/opt/left4me/src/scripts/{libexec,sbin}/` — no verbatim copy in this
# bundle's files/ tree. Sudoers (further below) lists the specific
# paths that left4me may invoke as root NOPASSWD.

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

symlinks = {
    '/etc/sysctl.d/99-left4me.conf': {
        'target': '/opt/left4me/src/deploy/files/etc/sysctl.d/99-left4me.conf',
        'owner': 'root',
        'group': 'root',
        'needs': [
            'git_deploy:/opt/left4me/src',
        ],
        'triggers': [
            'action:left4me_sysctl_reload',
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
            'cd /var/lib/left4me/steam && '
            'curl -fsSL https://media.steampowered.com/installer/steamcmd_linux.tar.gz | '
            'tar -xz'
            '"'
        ),
        'unless': 'test -x /var/lib/left4me/steam/steamcmd.sh',
        'cascade_skip': False,
        'needs': [
            'directory:/var/lib/left4me/steam',
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
            # Rebuild + reinstall the packages whenever the checkout
            # changes. pip_install does its own out-of-tree build (copies
            # source to a left4me-owned tempdir before invoking pip), so
            # the source tree itself stays root-owned and untouched.
            # pip_install cascades into alembic_upgrade → web restart.
            'action:left4me_pip_install',
            # alembic upgrade head is idempotent — keeping it as a direct
            # trigger off git_deploy is belt-and-braces in case the
            # pip_install cascade is ever short-circuited.
            'action:left4me_alembic_upgrade',
            # Privileged-helper scripts: reinstall from the new checkout
            # into /usr/local/{libexec,sbin}/ as root-owned. No-op when
            # the checkout didn't actually change (action is triggered).
            'action:install_left4me_scripts',
        ],
    },
}

actions['install_left4me_scripts'] = {
    # Copy privileged scripts from the deployed left4me checkout into
    # /usr/local/{libexec,sbin}/ as root:root 0755. Source of truth for
    # the file content is left4me's scripts/{libexec,sbin}/ tree (these
    # are application code, not deploy artifacts; left4me's deploy/ is
    # reference material only). The two install globs map source dirs
    # 1:1 to deploy targets. Triggered only on git_deploy updates so a
    # no-op apply doesn't re-copy.
    'command': (
        'install -m 0755 -o root -g root -t /usr/local/libexec/left4me/ '
        '/opt/left4me/src/scripts/libexec/*; '
        'install -m 0755 -o root -g root -t /usr/local/sbin/ '
        '/opt/left4me/src/scripts/sbin/*'
    ),
    'triggered': True,
    'cascade_skip': False,
    'needs': [
        'git_deploy:/opt/left4me/src',
        'directory:/usr/local/libexec/left4me',
    ],
}

actions['left4me_create_venv'] = {
    'command': 'sudo -u left4me /usr/bin/python3 -m venv /var/lib/left4me/.venv',
    'unless':  'test -x /var/lib/left4me/.venv/bin/python',
    'cascade_skip': False,
    'needs': [
        'directory:/var/lib/left4me',
        'pkg_apt:python3-venv',
        'user:left4me',
    ],
    'triggers': [
        'action:left4me_pip_upgrade',
    ],
}

actions['left4me_pip_upgrade'] = {
    'command': 'sudo -u left4me /var/lib/left4me/.venv/bin/python -m pip install --upgrade pip',
    'triggered': True,
    'cascade_skip': False,
    'needs': [
        'pkg_apt:python3-pip',
    ],
    # No triggers — pip_install is driven by git_deploy on actual code
    # updates, not by venv setup. Keeps pip_upgrade scoped to exactly
    # its purpose.
}

actions['left4me_pip_install'] = {
    # Non-editable install of l4d2host + l4d2web into the venv. We have
    # to copy the source to a left4me-writable tempdir first because
    # setuptools.build_meta writes <pkg>.egg-info/ into the source dir
    # during `get_requires_for_build_wheel`, and the source tree is
    # root-owned. cp -r is fast (small tree, world-readable), the build
    # itself happens in $tmpdir, and pip installs the resulting wheel
    # into /var/lib/left4me/.venv/site-packages. --force-reinstall
    # because the version string in pyproject.toml (0.1.0) doesn't
    # change commit-to-commit; without it pip would skip on no-op.
    # triggered:True so this only fires on actual git_deploy changes
    # (the cp + build is too heavy to run on every apply).
    'command': """sudo -u left4me sh -c '
set -e
tmpdir=$(mktemp -d -t left4me-build-XXXXXX)
trap "rm -rf \\"$tmpdir\\"" EXIT
cp -r /opt/left4me/src/l4d2host /opt/left4me/src/l4d2web "$tmpdir/"
/var/lib/left4me/.venv/bin/pip install --force-reinstall "$tmpdir/l4d2host" "$tmpdir/l4d2web"
'""",
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
        '/var/lib/left4me/.venv/bin/alembic -c /opt/left4me/src/l4d2web/alembic.ini upgrade head'
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
        '/var/lib/left4me/.venv/bin/flask --app l4d2web.app:create_app '
        'seed-script-overlays /opt/left4me/src/examples/script-overlays'
        '"'
    ),
    'triggered': True,
    'cascade_skip': False,
    'needs': [
        'action:left4me_alembic_upgrade',
    ],
}
