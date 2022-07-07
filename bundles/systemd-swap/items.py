size_mb = node.metadata.get('systemd-swap')//1_000_000

actions = {
    'stop_swap': {
        'command': f'systemctl stop swapfile.swap',
        'unless': f'! systemctl is-active swapfile.swap',
        'triggered': True,
    },
    'remove_swapfile': {
        'command': f'rm /swapfile',
        'unless': f'! test -e /swapfile',
        'triggered': True,
        'needs': {
            'action:stop_swap',
        },
    },
    'create_swapfile': {
        'command': f'dd if=/dev/zero of=/swapfile bs=1000000 count={size_mb}',
        'unless': f'stat -c %s /swapfile | grep ^{size_mb*1_000_000}$',
        'preceded_by': {
            'action:stop_swap',
            'action:remove_swapfile',
        },
        'triggers': {
            'action:initialize_swapfile',
            'svc_systemd:swapfile.swap:restart',
        },
    },
    'swapfile_mode': {
        'command': f'chmod 600 /swapfile',
        'unless': f'stat -c "%a" /swapfile | grep -q "^600$"',
        'needs': {
            'action:create_swapfile',
        },
        'triggers': {
            'svc_systemd:swapfile.swap:restart',
        },
    },
    'initialize_swapfile': {
        'command': f'mkswap /swapfile',
        'triggered': True,
        'needs': {
            'action:swapfile_mode',
        }
    },
}

svc_systemd = {
    'swapfile.swap': {
        'preceded_by': {
            'action:initialize_swapfile',
        },
        'needs': {
            'action:initialize_swapfile',
            'action:systemd-reload',
        },
    },
}
