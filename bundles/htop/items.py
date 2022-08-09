files = {
    '/etc/htoprc.global': {
        'content_type': 'mako',
        'context': {
            'cpus_per_row': 4 if node.metadata.get('vm/threads', node.metadata.get('vm/cores', 1)) > 8 else 2,
        },
    },
}
