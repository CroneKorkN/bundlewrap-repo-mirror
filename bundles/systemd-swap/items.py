size = node.metadata.get('systemd-swap')
assert isinstance(size, int)

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
        'command': f'dd if=/dev/zero of=/swapfile bs={size} count=1',
        'unless': f'stat -c %s /swapfile | grep ^{size}$',
        'preceded_by': {
            'action:stop_swap',
            'action:remove_swapfile',
        },
        'triggers': {
            'action:initialize_swapfile',
            'svc_systemd:swapfile.swap:restart',
        },
    },
    'initialize_swapfile': {
        'command': f'mkswap /swapfile',
        'triggered': True,
        'needs': {
            'action:create_swapfile',
        }
    },
}

files = {
    '/swapfile': {
        'content_type': 'any', 
        'mode': '600',
        'triggers': {
            'svc_systemd:swapfile.swap:restart',
        },
    }
}

svc_systemd = {
    'swapfile.swap': {
        'preceded_by': {
            'action:initialize_swapfile',
        },
        'needs': {
            'file:/swapfile',
            'action:initialize_swapfile',
            'action:systemd-reload',
        },
    },
}
