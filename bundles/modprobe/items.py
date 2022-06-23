for module, options in node.metadata.get('modprobe').items():
    if not options:
        continue
    
    files['/etc/modprobe.d'] = {
        'source': 'modprobe.conf',
        'content_type': 'mako',
        'context': {
            'module': module,
            'options': options,
        },
        'mode': '0644',
    }
    
