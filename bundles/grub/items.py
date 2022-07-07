files = {
    '/etc/default/grub': {
        'content_type': 'mako',
        'context': {
            'timeout': node.metadata.get('grub/timeout'),
            'kernel_params': node.metadata.get('grub/kernel_params'),
        },
        'mode': '0644',
        'triggers': {
            'action:update-grub',
        },
    }
}

actions = {
    'update-grub': {
        'command': 'update-grub',
        'triggered': True,
    },
}