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
    '/etc/systemd/system/left4me-web.service.d': {
        'owner': 'root', 'group': 'root', 'mode': '0755',
    },
    '/etc/systemd/system/left4me-server@.service.d': {
        'owner': 'root', 'group': 'root', 'mode': '0755',
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

# Privileged helpers are delivered via target-side symlinks (see the
# `symlinks` dict below) pointing into the left4me checkout at
# `/opt/left4me/src/deploy/scripts/{libexec,sbin}/`. No verbatim copy
# in this bundle's files/ tree. Sudoers (further below) lists the
# specific paths that left4me may invoke as root NOPASSWD.

files = {
    '/etc/left4me/sandbox-resolv.conf': {
        'source': 'etc/left4me/sandbox-resolv.conf',
        'mode': '0644',
        'owner': 'root',
        'group': 'root',
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
    '/etc/systemd/system/left4me-web.service.d/10-hardening.conf': {
        'target': '/opt/left4me/src/deploy/files/etc/systemd/system/left4me-web.service.d/10-hardening.conf',
        'owner': 'root', 'group': 'root',
        'needs': [
            'directory:/etc/systemd/system/left4me-web.service.d',
            'git_deploy:/opt/left4me/src',
        ],
        'triggers': [
            'action:left4me_daemon_reload',
        ],
    },
    '/etc/systemd/system/left4me-server@.service.d/10-hardening.conf': {
        'target': '/opt/left4me/src/deploy/files/etc/systemd/system/left4me-server@.service.d/10-hardening.conf',
        'owner': 'root', 'group': 'root',
        'needs': [
            'directory:/etc/systemd/system/left4me-server@.service.d',
            'git_deploy:/opt/left4me/src',
        ],
        'triggers': [
            'action:left4me_daemon_reload',
        ],
    },
    '/etc/sudoers.d/left4me': {
        'target': '/opt/left4me/src/deploy/files/etc/sudoers.d/left4me',
        'owner': 'root', 'group': 'root',
        'needs': [
            'action:left4me_chmod_sudoers',
            'git_deploy:/opt/left4me/src',
        ],
        # sudo follows symlinks; with the target file at root:root 0440
        # in a root-owned source tree, sudo accepts it. No daemon-reload
        # equivalent — sudo re-reads /etc/sudoers.d/ on each invocation.
    },
}

# Helper script source paths (in left4me's checkout) → deployed-form paths.
# Each gets a symlink item merged into the symlinks dict above.
_LEFT4ME_LIBEXEC_SCRIPTS = (
    'left4me-overlay',
    'left4me-systemctl',
    'left4me-journalctl',
    'left4me-script-sandbox',
)
_LEFT4ME_SBIN_SCRIPTS = (
    'left4me',
)

for _script in _LEFT4ME_LIBEXEC_SCRIPTS:
    symlinks[f'/usr/local/libexec/left4me/{_script}'] = {
        'target': f'/opt/left4me/src/deploy/scripts/libexec/{_script}',
        'owner': 'root', 'group': 'root',
        'needs': [
            'directory:/usr/local/libexec/left4me',
            'action:left4me_chmod_scripts',
            'git_deploy:/opt/left4me/src',
        ],
    }

for _script in _LEFT4ME_SBIN_SCRIPTS:
    symlinks[f'/usr/local/sbin/{_script}'] = {
        'target': f'/opt/left4me/src/deploy/scripts/sbin/{_script}',
        'owner': 'root', 'group': 'root',
        'needs': [
            'action:left4me_chmod_scripts',
            'git_deploy:/opt/left4me/src',
        ],
    }

actions = {
    'left4me_sysctl_reload': {
        'command': 'sysctl --system >/dev/null',
        'triggered': True,
    },
    'left4me_daemon_reload': {
        'command': 'systemctl daemon-reload',
        'triggered': True,
        'cascade_skip': False,
    },
    'left4me_verify_hardening_dropins_loaded': {
        # Post-apply self-test: confirm systemd actually picked up the
        # hardening drop-ins we shipped via symlink. Catches the failure
        # mode where the symlink lands but daemon-reload didn't take or
        # someone manually unlinked the drop-in. For the gameserver template
        # we query an imaginary instance — systemd resolves drop-in paths
        # for `name@instance.service` against the template (`name@.service.d/`),
        # so the instance need not exist or ever have run.
        'command': (
            'systemctl show left4me-server@verify.service -p DropInPaths --value '
            '| tr " " "\\n" '
            '| grep -qx /etc/systemd/system/left4me-server@.service.d/10-hardening.conf '
            '&& '
            'systemctl show left4me-web.service -p DropInPaths --value '
            '| tr " " "\\n" '
            '| grep -qx /etc/systemd/system/left4me-web.service.d/10-hardening.conf'
        ),
        'cascade_skip': False,
        'needs': [
            'action:left4me_daemon_reload',
            'symlink:/etc/systemd/system/left4me-web.service.d/10-hardening.conf',
            'symlink:/etc/systemd/system/left4me-server@.service.d/10-hardening.conf',
        ],
    },
    'left4me_chmod_sudoers': {
        # sudo refuses sudoers.d entries that aren't 0440 (or 0400) root:root.
        # git_deploy extracts as root with the in-repo file mode; this action
        # is belt-and-braces in case the repo mode drifts. Idempotent via
        # the `unless` gate.
        'command': 'chmod 0440 /opt/left4me/src/deploy/files/etc/sudoers.d/left4me',
        'unless': 'test "$(stat -c %a /opt/left4me/src/deploy/files/etc/sudoers.d/left4me)" = "440"',
        'cascade_skip': False,
        'needs': [
            'git_deploy:/opt/left4me/src',
        ],
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
            # Re-sync the workspace whenever the checkout changes. uv reads
            # the committed uv.lock at /opt/left4me/src and installs both
            # workspace members (l4d2host, l4d2web) editable into
            # /var/lib/left4me/.venv. Hatchling's PEP 660 editable install
            # doesn't write to the source tree, so /opt/left4me/src stays
            # root-owned and untouched. uv_sync cascades into
            # alembic_upgrade → seed_overlays → web restart.
            'action:left4me_uv_sync',
            # alembic upgrade head is idempotent — keeping it as a direct
            # trigger off git_deploy is belt-and-braces in case the
            # uv_sync cascade is ever short-circuited.
            'action:left4me_alembic_upgrade',
            # Reload systemd unit definitions whenever the checkout changes;
            # handles updates to hardening drop-in content without requiring
            # a symlink change.
            'action:left4me_daemon_reload',
        ],
    },
}

actions['left4me_chmod_scripts'] = {
    # sudo invokes the helpers by absolute path under /usr/local/...;
    # those resolve to the checkout via the symlinks above. The target
    # files must be executable (mode 0755). git_deploy extracts with
    # the in-repo file modes; this action is belt-and-braces in case
    # any helper's repo mode regresses to 0644.
    'command': (
        'chmod 0755 '
        '/opt/left4me/src/deploy/scripts/libexec/* '
        '/opt/left4me/src/deploy/scripts/sbin/*'
    ),
    'unless': (
        '! find /opt/left4me/src/deploy/scripts -type f \\! -perm 755 -print -quit 2>/dev/null | grep -q .'
    ),
    'cascade_skip': False,
    'needs': [
        'git_deploy:/opt/left4me/src',
    ],
}

actions['left4me_install_uv'] = {
    # uv is not in Debian Trixie's apt archive (only experimental/sid).
    # Pin to a specific release; download the tarball + its SHA256
    # sibling from astral-sh/uv releases, verify, install to
    # /usr/local/bin. Idempotent via `unless` — only re-runs when the
    # pinned version changes (bump the constant in two places below).
    # Pattern matches left4me_install_steamcmd (curl+tar) elsewhere in
    # this bundle. Bump cadence: as needed; both dev (brew uv) and
    # prod should track the same minor.
    'command': """set -e
tmpdir=$(mktemp -d); trap "rm -rf $tmpdir" EXIT
base=https://github.com/astral-sh/uv/releases/download/0.11.8
tar=uv-x86_64-unknown-linux-gnu.tar.gz
curl -fsSL -o $tmpdir/$tar        $base/$tar
curl -fsSL -o $tmpdir/$tar.sha256 $base/$tar.sha256
(cd $tmpdir && sha256sum -c $tar.sha256)
tar -xzf $tmpdir/$tar -C $tmpdir --strip-components=1
install -m 0755 $tmpdir/uv  /usr/local/bin/uv
install -m 0755 $tmpdir/uvx /usr/local/bin/uvx
""",
    'unless': '/usr/local/bin/uv --version 2>/dev/null | grep -qx "uv 0.11.8"',
    'cascade_skip': False,
    'needs': [
        'pkg_apt:curl',
    ],
    # No triggers — install_uv is a one-shot bootstrap. uv_sync needs
    # it (via `needs`), so the dependency runs install_uv first on a
    # clean host. After that, this action is a no-op on every apply
    # unless the version pin changes.
}

actions['left4me_uv_sync'] = {
    # The whole "install/refresh the workspace" deploy step, in one
    # action. uv reads /opt/left4me/src/uv.lock + the workspace's
    # pyproject.toml and installs both members (l4d2host, l4d2web)
    # editable into /var/lib/left4me/.venv. Hatchling's PEP 660
    # editable install drops a .pth pointing at the source tree — no
    # writes to source, so the root-owned /opt/left4me/src stays clean.
    #
    # UV_PROJECT_ENVIRONMENT redirects uv's default venv path
    # (<project>/.venv) to our writable runtime location. HOME is set
    # explicitly so uv's cache lands in /var/lib/left4me/.cache/uv
    # instead of the inherited sudo HOME (which can be unwritable for
    # the left4me user). cd /var/lib/left4me ensures uv's project-config
    # walk-up doesn't trip over an unreadable parent (e.g., /root or
    # /home/ckn). --frozen requires uv.lock to be present and
    # consistent with pyproject.toml — refuses to silently update the
    # lockfile during deploy.
    'command': (
        'sudo -u left4me sh -c "'
        'cd /var/lib/left4me && '
        'env HOME=/var/lib/left4me '
        'UV_PROJECT_ENVIRONMENT=/var/lib/left4me/.venv '
        '/usr/local/bin/uv sync --frozen --project /opt/left4me/src'
        '"'
    ),
    'triggered': True,
    'cascade_skip': False,
    'needs': [
        'git_deploy:/opt/left4me/src',
        'action:left4me_install_uv',
        'directory:/var/lib/left4me',
        'user:left4me',
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
        'env JOB_WORKER_ENABLED=false '
        '/var/lib/left4me/.venv/bin/alembic -c /opt/left4me/src/l4d2web/alembic.ini upgrade head'
        '"'
    ),
    'triggered': True,
    'cascade_skip': False,
    'needs': [
        'action:left4me_uv_sync',
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
        'env JOB_WORKER_ENABLED=false '
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
