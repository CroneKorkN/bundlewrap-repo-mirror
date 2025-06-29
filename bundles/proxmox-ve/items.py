files = {
    '/etc/apt/apt.conf.d/10pveapthook': {
        'content_type': 'any',
        'mode': '0644',
    },
    '/etc/apt/apt.conf.d/76pveconf': {
        'content_type': 'any',
        'mode': '0444',
    },
    '/etc/apt/apt.conf.d/76pveproxy': {
        'content_type': 'any',
        'mode': '0444',
    },
    '/etc/network/interfaces': {
        'content_type': 'any',
    },
}

symlinks['/etc/ssh/ssh_host_rsa_key.pub'] = {
    'target': '/etc/ssh/ssh_host_managed_key.pub',
}
