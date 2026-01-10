files = {
    # https://mikrotik.com/download/tools
    '/usr/share/snmp/mibs/MIKROTIK-MIB.txt': {
        'source': 'mikrotik.mib',
        'content_type': 'binary',
        'mode': '0644',
        'needed_by': {
            'svc_systemd:telegraf.service',
        },
    },
}
