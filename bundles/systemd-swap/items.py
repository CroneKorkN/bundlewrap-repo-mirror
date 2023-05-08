size = node.metadata.get('systemd-swap')

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
        'command': f'fallocate -l {size} /swapfile',
        'unless': f'stat -c %s /swapfile | grep ^{size}$',
        'preceded_by': {
            'action:stop_swap',
            'action:remove_swapfile',
        },
        'triggers': {
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
        'unless': 'blkid -o value -s TYPE /swapfile | grep -q "^swap$"',
        'needs': {
            'action:swapfile_mode',
        }
    },
}

svc_systemd = {
    'swapfile.swap': {
        'needs': {
            'action:initialize_swapfile',
            'action:systemd-reload',
        },
    },
}
