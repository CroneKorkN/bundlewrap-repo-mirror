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
